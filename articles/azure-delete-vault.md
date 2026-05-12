---
title: "AzureのRecovery Services Vault を安全に削除する手順"
emoji: "🔓"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "powershell", "RecoveryServicesVault"]
published: true
published_at: 2026-05-12 21:05
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

## 手順

### 1. PowerShell で Azure にサインインする

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


---

### 2. PowerShellスクリプトを作成する

以下に示したスクリプトは記事用のサンプルとして、サブスクリプション、リソースグループ、Vault 名をサンプル値で埋めています。  
実行前に読者が置き換える必要があるのは、これらの値と `<アカウントID>` だけです。


```powershell
 $ErrorActionPreference = 'Stop'

 # Vault をクリーンアップする対象の Azure リソースと利用アカウント。
 $subscriptionId = '00000000-0000-0000-0000-000000000000'
 $resourceGroupName = 'rg-example-backup'
 $vaultName = 'vault-example001'
 $accountId = '<アカウントID>'
 $vaultId = "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.RecoveryServices/vaults/$vaultName"

try {
     # まず現在の Az コンテキストを確認し、使い回せるログイン状態があるか調べる。
     $context = Get-AzContext -ErrorAction SilentlyContinue
     $needsLogin = $true

     # 既存コンテキストが対象サブスクリプションを向いている場合だけ再利用候補にする。
     if ($context -and $context.Subscription.Id -eq $subscriptionId) {
         try {
             # アクセストークンがまだ有効なら再ログインせず、そのまま処理を続ける。
             Get-AzAccessToken -ErrorAction Stop | Out-Null
             $needsLogin = $false
         }
         catch {
             # コンテキストが残っていてもトークン期限切れなら再ログインが必要。
             $needsLogin = $true
         }
     }

     if ($needsLogin) {
         # 必要な場合だけログインし直す。WAM を無効化し古いログイン状態を消してから
         # device code 認証で対象アカウントにサインインする。
         Update-AzConfig -EnableLoginByWam $false -Scope Process -ErrorAction SilentlyContinue | Out-Null
         Disconnect-AzAccount -Scope Process -ErrorAction SilentlyContinue | Out-Null
         Clear-AzContext -Scope Process -Force -ErrorAction SilentlyContinue
         Write-Host "Signing in as $accountId with device authentication..." -ForegroundColor Cyan
         Connect-AzAccount -AccountId $accountId -UseDeviceAuthentication | Out-Null
     }

     # ログイン後は毎回対象サブスクリプションへ切り替え、安全のため結果も確認する。
     Write-Host "Switching to subscription $subscriptionId..." -ForegroundColor Cyan
     Set-AzContext -SubscriptionId $subscriptionId | Out-Null

     $currentContext = Get-AzContext
     if (-not $currentContext -or $currentContext.Subscription.Id -ne $subscriptionId) {
         throw "Subscription $subscriptionId is not available for account $accountId."
     }

     # この登録が残っていると Vault 削除のブロッカーになるため、先に列挙して解除する。
     Write-Host "Unregistering Storage containers in vault $vaultId..." -ForegroundColor Yellow
     $StorageAccounts = Get-AzRecoveryServicesBackupContainer -ContainerType AzureStorage -VaultId $vaultId

     if (-not $StorageAccounts) {
         # 解除対象がなければ、このスクリプトでやることは完了。
         Write-Host 'No Storage containers found.' -ForegroundColor Yellow
         exit 0
     }

     # 各 Storage コンテナーの登録を解除し、Vault を削除できる状態に近づける。
     foreach ($item in $StorageAccounts) {
         Write-Host "Unregistering Storage container: $($item.Name)" -ForegroundColor DarkYellow
         Unregister-AzRecoveryServicesBackupContainer -Container $item -Force -VaultId $vaultId
     }

     Write-Host 'All Storage containers unregistered.' -ForegroundColor Green
 }
 catch {
     # 失敗理由をそのまま表示し、呼び出し元が失敗を検知できるよう非ゼロで終了する。
     Write-Error $_
     exit 1
 }
```

このスクリプトでは、以下のことをやっているために長いコードになってます。

- ログイン済みでない場合は、ログイン処理を行っている
- 誤ったサブスクリプションで削除操作が走るのを防ぐ処理を入れている
- エラーハンドリングを try/catch で囲んでいる


本質的なコードは、以下のコードになります。

```
    $StorageAccounts = Get-AzRecoveryServicesBackupContainer -ContainerType AzureStorage -VaultId $vaultId
    foreach ($item in $StorageAccounts) {
         Write-Host "Unregistering Storage container: $($item.Name)" -ForegroundColor DarkYellow
         Unregister-AzRecoveryServicesBackupContainer -Container $item -Force -VaultId $vaultId
    }
```


---

### 3. Storage Container の登録を解除する

Recovery Services コンテナー が消せない原因になりやすいのが、Backup 用に登録された Storage Container です。  
前述のPowerShellスクリプトを使って解除しました。


実行結果として、以下のように出れば成功です。

```
All Storage containers unregistered.
```

今回もこの状態になり、Storage Container の登録解除は完了しました。


なお、Azureにログインしていない状態でこのスクリプトを実行したときは、以下のようなメッセージが出ます。

```
[Login to Azure] To sign in, use a web browser to open the page 
https://login.microsoft.com/device and enter the code H3K9CBPDE to authenticate.
```

表示されているURLをブラウザで開き、このコード`H3K9CBPDE`を入れて、Azureにログインします。

複数のサブスクリプションがある場合あｈ、サブスクリプションの選択が表示されますので、該当するサブスクリプションを選択します。

選択すると、本来の削除処理が走ります。


---

### 4. ポータルで Recovery Services コンテナー を削除する

Storage Container の登録解除後、Azure Portal から対象 Recovery Services コンテナー を削除します。

ここで大事なのは、**Recovery Services コンテナー の削除は非同期** だという点です。  
削除ボタンを押しても、その場ですぐ消えるとは限りません。

つまり、

- ポータルで削除操作をした
- でもリソースグループ内にしばらく残って見える

というのは、**直後であれば正常なことがあります**。

---

### 5. 削除完了を確認する

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

何も返らなければ、コンテナーは削除されています。

---

## まとめ

Recovery Services コンテナー を消すときは、**いきなり Recovery Services コンテナー を削除しようとしない**のが重要です。  
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


## おまけ


実は、前述のPowerShellスクリプトの原型は、AzureのCopilotに作成してもらったものです。

「特定の依存関係が無いのに、コンテナーが削除できないので、削除するための方法を教えてください」

のようなプロンプトをAzureポータルのCopilotを使って作成してもらいました。それが以下のコードです。

しかし、このままでは動かず


```powershell
# Unregister Storage containers from Recovery Services Backup
Write-Host "Switching to subscription $subscriptionId..." -ForegroundColor Cyan
Set-AzContext -SubscriptionId  $subscriptionId = 00000000-0000-0000-0000-000000000000
Write-Host "Unregistering Storage containers in vault $vaultId..." -ForegroundColor Yellow
$StorageAccounts = Get-AzRecoveryServicesBackupContainer -ContainerType AzureStorage -VaultId /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-gpt/providers/Microsoft.RecoveryServices/vaults/vault-lyqsj7qh
foreach ($item in $StorageAccounts) {
        Write-Host "Unregistering Storage container: $($item.Name)" -ForegroundColor DarkYellow
        Unregister-AzRecoveryServicesBackupContainer -container $item -Force -VaultId /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001
}
Write-Host "All Storage containers unregistered." -ForegroundColor Green
```