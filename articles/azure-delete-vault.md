# Recovery Services Vault を安全に削除する手順まとめ  
Azure Backup の Storage Container 登録解除から Vault 削除完了まで

Azure の `Recovery Services Vault` は、ポータルでそのまま削除しようとしても消えないことがあります。  
原因の多くは、**バックアップ対象の登録が残っている**ことです。

今回は、`AzureStorage` の登録を解除してから `vault-example001` を削除し、最終的に削除完了まで確認できたので、**成功する流れを先に**まとめます。

---

## 前提

今回の対象は以下です。

- サブスクリプション: `00000000-0000-0000-0000-000000000000`
- リソースグループ: `rg-example-backup`
- Vault: `vault-example001`

---

## 全体の流れ

やることは次の 4 ステップです。

1. Azure に正しいアカウントでサインインする  
2. Vault に登録されている Storage Container を解除する  
3. ポータルで Vault を削除する  
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

Vault が消せない原因になりやすいのが、Backup 用に登録された Storage Container です。  
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

## 3. ポータルで Vault を削除する

Storage Container の登録解除後、Azure Portal から対象 Vault を削除します。

ここで大事なのは、**Delete Vault は非同期** だという点です。  
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

## 今回の成功パターン

今回うまくいった流れをそのまま書くと、次の通りです。

1. `pwsh` で Azure にサインイン
2. `Set-AzContext` で対象サブスクリプションへ切り替え
3. delvault_blog.ps1 を実行
4. Storage Container の `UnRegister Completed` を確認
5. Azure Portal で Vault を削除
6. Activity Log で `Delete Vault Started / Accepted` を確認
7. 少し待つ
8. 最終的に Vault がリソースグループから消えたことを確認

この流れで、最終的に削除完了まで到達できました。

---

# トラブルシューティング

ここからは、途中で遭遇しやすいポイントです。

## 1. `.ps1` 実行でエラーになる

`bash` や `Git Bash` から delvault_blog.ps1 を直接実行すると、環境の違いで失敗しやすいです。  
**PowerShell (`pwsh`) で実行**するのが安全です。

```powershell
.\delvault_blog.ps1
```

---

## 2. Azure ログインまわりで失敗する

アカウントやテナントの食い違いがあると、ログイン後に意図しないサブスクリプションが選ばれることがあります。  
ログイン後に `Get-AzContext` で確認し、必要なら `Set-AzContext` を実行します。

```powershell
Get-AzContext
```

```powershell
Set-AzContext -SubscriptionId "00000000-0000-0000-0000-000000000000"
```

---

## 3. `Get-AzRecoveryServicesBackupContainer` で `-Status` が使えない

環境によっては、次のように `-Status` パラメーターが使えません。

> A parameter cannot be found that matches parameter name 'Status'

その場合は、まず取得してから `Where-Object` で絞り込みます。

```powershell
Get-AzRecoveryServicesBackupContainer -ContainerType AzureStorage -VaultId "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001" | Where-Object { $_.RegistrationStatus -eq "Registered" -or $_.Status -eq "Registered" } | Select-Object FriendlyName, RegistrationStatus, Status
```

全件確認したい場合はこちらです。

```powershell
Get-AzRecoveryServicesBackupContainer -ContainerType AzureStorage -VaultId "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001" | Format-Table FriendlyName, RegistrationStatus, Status, ContainerType -AutoSize
```

---

## 4. ポータルで削除したのに Vault が残る

これは **すぐには異常とは限りません**。  
Recovery Services Vault の削除は非同期です。

確認ポイントは以下です。

- `Delete Vault Started`
- `Delete Vault Accepted`
- でも `Delete Vault Succeeded` はまだ見えていない

この場合、**削除処理が進行中**です。  
少し待って再確認します。

```powershell
Get-AzLog -ResourceId "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001" | Select-Object EventTimestamp, OperationName, Status, SubStatus | Format-Table -AutoSize
```

---

## 5. Vault がずっと消えない

この場合は、まだ削除をブロックする要素が残っている可能性があります。  
たとえば、別の Backup Container や保護項目、Vault 側設定などです。

まずはコンテナー一覧を確認します。

```powershell
$vaultId="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example-backup/providers/Microsoft.RecoveryServices/vaults/vault-example001"; Get-AzRecoveryServicesBackupContainer -VaultId $vaultId | Format-Table FriendlyName, ContainerType, BackupManagementType, RegistrationStatus, Status -AutoSize
```

---

# まとめ

Recovery Services Vault を消すときは、**いきなり Vault を削除しようとしない**のが重要です。  
先に依存関係、特に **Storage Container の登録解除** を行うと、削除までスムーズに進みます。

今回の実績ベースでは、次の順番が正解でした。

1. `pwsh` で実行する  
2. 正しい Azure サブスクリプションに切り替える  
3. delvault_blog.ps1 で Storage Container を解除する  
4. ポータルで Vault を削除する  
5. Activity Log を見ながら非同期削除の完了を待つ  

最終的に `vault-example001` は正常に削除されました。

- 置換が必要: `delvault_blog.ps1` の `<アカウントID>`
- サンプル値のままでよい箇所: サブスクリプション ID、リソースグループ名、Vault 名