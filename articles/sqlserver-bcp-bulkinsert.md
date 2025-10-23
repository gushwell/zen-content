---
title: "SQL Serverで特定テーブルを別DBへ“そっくり移す”手順（bcp + BULK INSERT）"
emoji: "👥"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["sqlserver", "db"]
published: true
published_at: 2025-11-18 08:15
publication_name: zead
---



## はじめに

この記事では、SQL Server の bcp と BULK INSERT を使って、あるデータベースの特定テーブルを別のデータベースへ同一スキーマのまま丸ごとコピーする手順をまとめます。実運用で「本番の最新データをテスト環境で検証したい」といったケースを想定しています。


### サンプル環境の名前（置換後）

- ソースサーバー: PROD-SQL01（必要に応じて PROD-SQL01\SQL2019 のようなインスタンス名）
- ターゲットサーバー: TEST-SQL01
- ソースDB: SampleSourceDb
- ターゲットDB: SampleTargetDb
- テーブル: dbo.MailTemplates
- 作業用フォルダー（ターゲット側）: C:\work
- bcp ファイル名（例）: C:\work\MailTemplates_Source.bcp（ソースからのエクスポート）
- ターゲット既存データのバックアップ bcp: C:\work\MailTemplates_TargetBackup.bcp

#### サーバー名／インスタンス名の確認

SSMS で接続後、以下で確認できます。

```sql
SELECT SERVERPROPERTY('MachineName') AS ServerName,
       SERVERPROPERTY('InstanceName') AS InstanceName;
````


## 手順

### 0. 前提条件

* 管理者権限（対象DBの SELECT/TRUNCATE/ BULK INSERT 権限、ファイルシステム権限）
* bcp ユーティリティと SSMS が利用可能
* ターゲットDBとターゲットテーブルのスキーマがソースと一致\
  テーブル定義（列順・型・NULL 可否など）はソース／ターゲットで同一であることが前提
* 作業フォルダー C:\work を用意（SQL Server サービス アカウントに読み取り権限）
* Linux 版を利用する場合は、`/var/opt/mssql/data` など SQL Server サービス アカウントがアクセスできるパスを用意すること。

### 1. ターゲット側の事前バックアップ（必須）

事前にターゲット側のバックアップを必ず取得してください（テーブルのbcpバックアップ＋DBのフルバックアップ）。


#### 1-1) テーブルの中身を bcp でバックアップ（PowerShell/CMD どちらでも可）

Windows 認証を使う場合の例（推奨）：

```powershell
bcp "SampleTargetDb.dbo.[MailTemplates]" out "C:\work\MailTemplates_TargetBackup.bcp" -S TEST-SQL01 -T -w
```

SQL 認証を使う場合：

```powershell
bcp "SampleTargetDb.dbo.[MailTemplates]" out "C:\work\MailTemplates_TargetBackup.bcp" -S TEST-SQL01 -U sa -P <Password> -w
```

**ポイント**

* -w は Unicode 文字形式での入出力（bcp の推奨オプション）
* 完全修飾名（<DB>.<schema>.<table>）で指定すれば -d は省略可

#### 1-2) ターゲットDBのフルバックアップ（SSMS）

* SSMS でターゲットサーバーに接続
* Databases > SampleTargetDb を右クリック > Tasks > Back Up...
* Backup type: Full を選択、出力先を確認して実行
  例: C:\Program Files\Microsoft SQL Server\MSSQLXX.MSSQLSERVER\MSSQL\Backup
  必要なら「Script」ボタンで T-SQL を保存しておくと再実行が容易です。

### 2. ソース側テーブルを bcp でエクスポート

Windows 認証例：

```powershell
bcp "SampleSourceDb.dbo.[MailTemplates]" out "C:\work\MailTemplates_Source.bcp" -S PROD-SQL01 -T -w
```

SQL 認証例：

```powershell
bcp "SampleSourceDb.dbo.[MailTemplates]" out "C:\work\MailTemplates_Source.bcp" -S PROD-SQL01 -U sa -P <Password> -w
```

**メモ**

* -w（Unicode）でエクスポートすると、後段の BULK INSERT では DATAFILETYPE='widechar' を指定して整合させます。

### 3. bcp ファイルをターゲットサーバーへコピー

* 例: C:\work\MailTemplates\_Source.bcp を TEST-SQL01 の C:\work\ に配置
  Linux 環境では `/var/opt/mssql/data` など適切なパスに配置。
* SQL Server サービス アカウントが読み取れることを確認（アクセス権に注意）

### 4. ターゲットDBへインポート（SSMS で T-SQL 実行）

```sql
SET XACT_ABORT ON;
BEGIN TRAN;
TRUNCATE TABLE dbo.MailTemplates;

BULK INSERT dbo.MailTemplates
FROM 'C:\work\MailTemplates_Source.bcp'  -- Linuxの場合は '/var/opt/mssql/data/…'
WITH (
  DATAFILETYPE = 'widechar',
  KEEPIDENTITY,
  TABLOCK,
  BATCHSIZE = 10000,
  CHECK_CONSTRAINTS,
  FIRE_TRIGGERS,
  MAXERRORS = 0
);

-- IDENTITY reseed（increment=1 の想定）
DECLARE @maxId BIGINT = ISNULL((SELECT MAX(Id) FROM dbo.MailTemplates), 0);
DBCC CHECKIDENT ('dbo.MailTemplates', RESEED, @maxId);

COMMIT;

-- 大量データ投入後は統計情報を更新しておくとクエリ性能が安定
EXEC sp_updatestats;
```

**オプションの意味**

* DATAFILETYPE='widechar': bcp -w と整合（Unicode 文字形式）
* KEEPIDENTITY: bcp ファイルに含まれる IDENTITY 値を維持
* TABLOCK: 挿入時にテーブルロックを取り、パフォーマンスを向上
* BATCHSIZE: コミット単位の調整（環境に応じて変更可）


### 5. 付随スクリプトの実行（必要な場合）

* 例: 参照データの整合やバージョンアップ用の SQL（UpdateAfterImport.sql など）を実行
* 実行内容・順序はアプリケーションの運用手順に従ってください

### 6. 検証

* 行数一致の確認

  ```sql
  SELECT COUNT(*) FROM SampleSourceDb.dbo.MailTemplates;  -- ソース
  SELECT COUNT(*) FROM SampleTargetDb.dbo.MailTemplates;  -- ターゲット
  ```
* 代表データの spot check

  ```sql
  SELECT TOP(10) * FROM SampleTargetDb.dbo.MailTemplates ORDER BY <主キー>;
  ```
* 必要ならチェックサムや件名・更新日時などのキー列比較で追加検証

### 7. ロールバック手順（万一に備えて）

* テーブルだけ戻す場合: 1-1 で取ったテーブル bcp を BULK INSERT で復元

```sql
  USE SampleTargetDb;
  GO
  TRUNCATE TABLE dbo.MailTemplates;
  BULK INSERT dbo.MailTemplates
  FROM 'C:\work\MailTemplates_TargetBackup.bcp'
  WITH (DATAFILETYPE='widechar', KEEPIDENTITY, TABLOCK);
  EXEC sp_updatestats;  -- 統計情報を更新
```

* DB 全体を戻す場合: 1-2 のフルバックアップから RESTORE（運用手順に従う）

## よくあるハマりどころと対策

* アクセス権エラー: BULK INSERT はSQL Serverサービス アカウントから見たパス権限が必要。C:\work などローカルに配置して権限を付与。Linuxの場合は `/var/opt/mssql/data` など適宜。
* 文字化け: bcp 出力 -w と BULK INSERT の DATAFILETYPE='widechar' をセットで使う。
* IDENTITY がずれる: BULK INSERT に KEEPIDENTITY を付与。必要なら最後に DBCC CHECKIDENT で確認。
* 制約/トリガーの影響: 大量投入中に制約やトリガーでエラーが出る場合がある。必要に応じて一時的に無効化（運用ポリシーに従う）やステージングテーブルの利用を検討。
* インスタンス名が分からない: 冒頭の SERVERPROPERTY クエリで確認。
* 形式ファイルが必要か: 今回は同一スキーマ前提のため不要。列順や型が異なる場合は bcp のフォーマットファイル（.fmt/.xml）でマッピングが必要。
* 大量インポート後は `sp_updatestats` などで統計情報を更新し、クエリ計画の劣化を防ぐ。

## 参考（要点）

* bcp の -w は Unicode 文字形式（推奨）。BULK INSERT 側は DATAFILETYPE='widechar' を指定すると対応します。
* IDENTITY の維持は BULK INSERT なら KEEPIDENTITY（bcp in なら -E）。
* SSMS からは簡単に DB フルバックアップが可能。デフォルトのバックアップ先はインスタンス設定に依存します。
* Linux 版 SQL Server ではパスの指定や権限が異なるため、`/var/opt/mssql/data` などサービスアカウントが読み書き可能な場所を指定します。

## 補足

* セキュリティ上、サンプルでは -U/-P を使っていますが、可能なら Windows 認証（-T）や資格情報の安全な管理を推奨します。
* 同一インスタンス内で DB 間コピーが目的で、件数が少ない場合は INSERT ... SELECT でも対応可能です。大量データや文字列の互換性・速度重視なら本記事の方法が有効です。

## 最後に

この手順を、対象テーブル名・サーバー名・パスに合わせて置き換えれば、そのまま実施できます。テーブルに外部キーやトリガーがある場合、投入順や無効化の有無など運用ルールはありますか？必要であればその前提も組み込んだうえで手順を微調整します。


