---
title: "Foundry のモデル入力は学習に使われる？（Azure Direct と Foundry 経由 Claude の違い）"
emoji: "🧰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "foundry", "llm", "calude", "openai" ]
published: true
published_at: 2026-01-13 08:30
publication_name: zead
---

## はじめに

Microsoft Foundry（Azure AI Foundry / Foundry classic）で生成 AI を使うとき、気になるのはだいたいこの 2 つです。

- 入力したデータ（プロンプト/出力）は **学習に使われるのか**
- 入力したデータは **どこで処理され得るのか**（海外に出るのか）

結論から言うと、Foundry のモデルは **“Azure Direct Models かどうか”**で前提が分かれます。  

企業で、Foundry のどのモデルを利用したらよいのかを決める際は、性能や価格の比較に入る前に、まずここを確認するのが良いと考えます。

---

## 結論（最短）

- **Azure Direct Models（Azure が直接提供）**  
  Microsoft Learn に **「プロンプト/出力は基盤モデルの学習・再学習・改善に使わない」**、**「モデルはステートレス」**と明記されています。  
  処理場所は原則 **顧客指定の geography（地理）**の範囲ですが、*Global / DataZone* などのデプロイ種別では“処理され得る場所”が広がり得ます。  
  出典：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic

- **Foundry 経由の Claude（Anthropic）**  
  Microsoft Learn に **「Anthropic（Microsoft ではない）がデータ処理者」**、**「プロンプト/出力は世界中で処理され得る」**と明記されています。  
  出典：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/claude-models/data-privacy?view=foundry-classic

---

## まず押さえる用語：処理（processing）と保存（at rest）は別

「海外に出る？」の議論がややこしくなるのは、**処理**と**保存**が混ざりやすいからです。

- **処理（processing）**：返答（出力）を作る計算が行われる場所
- **保存（at rest）**：履歴やアップロードデータ等が“残る”場所（機能によって発生）

:::message
Azure Direct Models でも、機能（例：Files / vector store / Threads / Stored completions 等）によっては保存が発生します。保存条件の確認は、まず公式ページを当たるのが安全です。  
https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic
:::

---

## 早見表（どっちがどっち？）

| 観点 | Azure Direct Models | Foundry 経由 Claude（Anthropic） |
|---|---|---|
| データ処理者 | Microsoft（Azure） | Anthropic（Microsoft ではない） |
| 学習に使われる？ | **使わない**（公式明記。許可/指示がない限り） | Microsoft Learn では **「使わない」と断言しない**（詳細は Anthropic 文書参照の立て付け） |
| 処理場所 | 原則 **顧客指定 geography 内**（ただし例外・デプロイ種別で広がり得る）<br >Azure内部で完結 | **世界中で処理され得る**（地域外含む） |
| モデルが覚える？ | **ステートレス**（公式明記） | 保存/スクリーニング等は Anthropic 文書参照 |



---

## チェックリスト（導入前に見るやつ）

社内利用・顧客データ取り扱いが絡む場合、最低限ここを確認しておくと後で揉めにくいです。

1. 使いたいモデルが **Azure Direct Models** かどうか
2. **処理場所**の前提（geography / Global / DataZone 等）を、設計・監査要件と照合できるか
3. **学習利用しない**ことを、どの“根拠（公式文言/契約）”で説明するのか
4. 保存が発生する機能（Files / vector store / Threads 等）を使う場合、**保存条件**も含めて説明できるか

---

## 「このモデルは Azure Direct Models なの？」を確かめる

ざっくりの実務手順は次のどちらかです。

- Foundry のモデルカタログで **“Direct from Azure”** 相当の絞り込み（UI は変わる可能性あり）
- 公式ドキュメントで **“sold directly by Azure”** に該当するか確認

参考：  
https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic

---

## FAQ

### Q. 「Foundry から呼べる」＝「Microsoft が全部面倒を見る」じゃないの？

違う場合があります。Foundry の UI から使えても、**データ処理者がモデル提供者（例：Anthropic）**になるモデルがあります。  
Microsoft Learn のページで、**processor（処理者）**が誰かを先に確認するのが確実です。

### Q. Azure Direct Models は “絶対に” geography の外で処理されない？

“地域外処理なし”のような言い切りは危険です。公式は「顧客指定 geography 内が原則」＋「運用上の例外」＋「デプロイ種別で広がり得る」をセットで説明しています。  

以下、その根拠となる原文。

> Prompts and responses are processed within the customer-specified geography (unless you are using a Global or DataZone deployment type), but may be processed between regions within the geography for operational purposes (including performance and capacity management). See below for information about location of processing when using a Global or DataZone deployment type.

> In addition to standard deployments, Foundry offers Azure Direct Model deployment options labeled as 'Global' and 'DataZone.' For any deployment type labeled 'Global,' prompts and responses may be processed in any geography where the relevant Azure Direct Model is deployed (learn more about region availability of models). For any deployment type labeled as 'DataZone,' prompts and responses may be processed in any geography within the specified data zone, as defined by Microsoft.


### Q. 「学習に使われない」って、具体的に何が嬉しいの？

企業利用でよく効くのは **説明責任**です。  
監査・規制・顧客要件に対し、「学習に使われない」ことを **公式文言**で説明できるかどうかで、選定の難易度が変わります。

以下、その根拠となる原文。

> are NOT used to train any generative AI foundation models without your permission or instruction

> Customer Data, Prompts, and Completions are NOT used to improve Microsoft or third-party products or services without your explicit permission or instruction.

> The models are stateless: no prompts or completions are stored in the model. Additionally, prompts and completions are not used to train, retrain, or improve the base models.

### Q. アップロードしたファイルの扱いは？

Azure Direct Modelsでは、推論処理のために一時的に保存されますが、長期保存はされません。保存する際は、暗号がされて保存されます。
なお、Azure Direct Models では、Microsoft の安全性基準に基づき 不正利用監視のために一時的にデータが保存される場合があります。
どのような場合であっても、長期保存はされませんし、他の顧客との共有は行われません。


---

## 参考リンク（公式）

- Azure Direct Models のデータ・プライバシー：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic
- Claude models のデータ・プライバシー：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/claude-models/data-privacy?view=foundry-classic
- Models sold directly by Azure：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic

## 最後に

Foundry 利用時のデータ取り扱いは、「モデル名」より先に **“Azure Direct Models かどうか”**で大枠が決まります。  
迷ったら Microsoft Learn のデータ・プライバシーのページを根拠にして、組織のポリシーに合うモデルを選ぶのが安全です。

もし内容に誤りがあれば、コメントで教えていただけると助かります。