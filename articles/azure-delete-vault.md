---
title: "AzureのRecovery Services Vault を安全に削除する手順"
emoji: "🔬"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "powershell", "RecoveryServicesValut"]
published: true
published_at: 2025-07-23 21:05
publication_name: zead
---

## はじめに

不要になった Azure のリソースグループを削除しようとしたら、`Recovery Services コンテナー(Recovery Services Vault)` の削除に失敗して、リソースグループの削除ができませんでした。

そのため、削除できなかった `Recovery Services コンテナー(Recovery Services Vault)` だけをポータルで削除しようとしましたが、やはり削除に失敗します。

詳しい原因までは突き止められませんでしたが、原因の多くは、**バックアップ対象の登録が残っている**ことのようです。

この記事では、`AzureStorage` の登録を解除してから `Recovery Services コンテナー` を削除できた手順をまとめています。なお、保護済みデータやソフト削除済みデータが残っている場合は、別の依存関係も解除が必要です。

※ Azure の日本語UIでは、英語の Recovery Services vault が「Recovery Services コンテナー」と翻訳されています。以降は Recovery Services コンテナー と書きます。



---

## 前提

今回の対象は以下です。

- サブスクリプション: `00000000-0000-0000-0000-000000000000`
- リソースグループ: `rg-example-backup`
- Recovery Services コンテナー: `vault-example001`

---

## 全体の流れ

やることは次の 4 ステップです。

1. Azure に正しいアカウントでサインインする  
2. Recovery Services コンテナー に登録されている Storage Container を解除する  
3. ポータルで Recovery Services コンテナー を削除する  
4. 削除完了を確認する  

---

## 1. PowerShell で Azure にサインインする

`.ps1` を扱うので、`bash` や `Git Bash` ではなく **PowerShell (`pwsh`)** で実行します。

```powershell
Connect-AzAccount
```

必要ならサブスクリプションを明示的に切り替えます。

```powershell
Set-AzContext -SubscriptionId "00000000-0000-0000-0000-000000000000"
```

現在のサブスクリプション確認です。

```powershell
Get-AzContext
```

`delvault_blog.ps1` は記事用のサンプルとして、サブスクリプション、リソースグループ、Vault 名をサンプル値で埋めています。  
実行前に読者が置き換える必要があるのは、基本的に `<アカウントID>` だけです。

---

## 2. Storage Container の登録を解除する

Recovery Services コンテナー が消せない原因になりやすいのが、Backup 用に登録された Storage Container です。  
今回は delvault_blog.ps1 を使って解除しました。

実行コマンドはこれです。

```powershell
.\delvault_blog.ps1
```

実行結果として、以下のように出れば成功です。

- `UnRegister Completed`
- `All Storage containers unregistered.`

今回もこの状態になり、Storage Container の登録解除は完了しました。

---

## 3. ポータルで Recovery Services コンテナー を削除する

Storage Container の登録解除後、Azure Portal から対象 Recovery Services コンテナー を削除します。

ここで大事なのは、**Delete Recovery Services コンテナー は非同期** だという点です。  
削除ボタンを押しても、その場ですぐ消えるとは限りません。

つまり、

- ポータルで削除操作をした
- でもリソースグループ内にしばらく残って見える

というのは、**直後であれば正常なことがあります**。

---

## 4. 削除完了を確認する

削除要求が通ったかどうかは、Azure Activity Log で確認できます。

```powershell
Get-AzLog -ResourceId "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001" | Select-Object EventTimestamp, OperationName, Status, SubStatus | Format-Table -AutoSize
```

途中では次のような状態になります。

- `Delete Vault Started`
- `Delete Vault Accepted`

この段階では、**まだ削除完了ではありません**。

その後、しばらくして実際にリソースが消えれば完了です。  
存在確認は次でもできます。

```powershell
Get-AzResource -ResourceGroupName "rg-example-backup" -ResourceType "Microsoft.RecoveryServices/vaults" -Name "vault-example001"
```

何も返らなければ、Vault は削除されています。

---

## まとめ

Recovery Services Recovery Services コンテナー を消すときは、**いきなり Recovery Services コンテナー を削除しようとしない**のが重要です。  
先に依存関係、特に **Storage Container の登録解除** を行うと、削除までスムーズに進みます。

今回うまくいった流れをそのまま書くと、次の通りです。

1. `pwsh` で Azure にサインイン
2. `Set-AzContext` で対象サブスクリプションへ切り替え
3. delvault_blog.ps1 を実行
4. Storage Container の `UnRegister Completed` を確認
5. Azure Portal で Recovery Services コンテナー を削除
6. Activity Log で `Delete Vault Started / Accepted` を確認
7. 少し待つ
8. 最終的に Recovery Services コンテナー がリソースグループから消えたことを確認

この流れで、最終的に削除完了まで到達できました。


