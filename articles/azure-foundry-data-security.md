---
title: "Azure Foundryで入力データは学習される？本当に安全？（Azure Direct と Foundry 経由 Claude の違い）"
emoji: "🧰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "foundry", "llm", "calude", "openai" ]
published: true
published_at: 2026-01-14 08:30
publication_name: zead
---


## はじめに  

### Microsoft Foundryの生成AIモデルとは

Microsoft Foundry（Azure AI Foundry / Foundry classic）は、複数の生成AIモデルを横断的に利用できるプラットフォームです。  
機能面では、生成AIのモデルルーティングを提供するサービスとして、OpenRouterに近い位置づけとも言えます。  
一方で、Microsoft Foundryはエンタープライズ利用を前提に設計されており、セキュリティ・データの取り扱い・リージョン制御に重点が置かれています。

Microsoft Foundryでは以下のようなモデルが利用可能です（一部のみ掲載）



### この記事の目的

Microsoft Foundryで利用できる生成AIモデルは大きく「Azure Direct Models」と「Foundry経由のモデル（例: Claude）」の2つに分かれます。  
本記事では、企業環境でMicrosoft Foundryを利用する際に「どのモデル群を選択すべきか」判断するための**前提条件を整理すること**を目的としています。  

具体的には以下の2点に焦点を当てて解説します。  
- 入力したデータ（プロンプト／生成結果）は**モデルの学習に利用されるのか**  
- 入力データは**どのリージョンで処理されるのか**（国外に送信される可能性はあるのか）

性能や価格の比較の前に、これらの違いを理解することが重要です。

---

## まず押さえる用語：処理（processing）と保存（at rest）は別

「海外に出る？」の議論がややこしくなるのは、**処理**と**保存**が混ざりやすいからです。  

- **処理（processing）**：返答（出力）を作る計算が行われる場所  
- **保存（at rest）**：履歴やアップロードデータ等が“残る”場所（機能によって発生）

:::message
Azure Direct Modelsでも、Files / vector store / Threads / Stored completions などの機能によっては保存が発生します。保存条件の確認は公式ページを参照してください。  
https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic  
:::

---

## 結論（短縮版）

- **Azure Direct Models（Azureが直接提供）**  
  Microsoftの文書では、Azure Direct Modelsに送られたプロンプトや出力は顧客の許可・指示なしに基盤モデルの学習・再学習・改善には使用されないと明記され、モデルはステートレスであると説明されています。ただし、FilesやStored completionsなど特定の機能ではデータがサービス内に保存され、監査や不正利用検知のためにサンプルが保存・人によるレビューされることがあります。  
  処理は原則、顧客指定のgeography（地理）内で行われますが、GlobalやDataZoneといったデプロイ種別や運用上の例外により他地域で処理される可能性もあります。  
  出典：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic  

- **Foundry経由の Claude（Anthropic）**  
  Microsoft Learnによれば、Anthropicがデータ処理者であり、プロンプトや出力は世界中の地域で処理され得ると明記されています。  
  出典：  
  https://learn.microsoft.com/ja-jp/azure/ai-foundry/responsible-ai/claude-models/data-privacy?view=foundry-classic  

---

## 早見表（どっちがどっち？）

| 観点          | Azure Direct Models                                    | Foundry経由 Claude（Anthropic）                     |
|---------------|-------------------------------------------------------|----------------------------------------------------|
| データ処理者  | Microsoft（Azure）                                    | Anthropic（Microsoftではない）                     |
| 学習に使われる？ | **顧客の許可なしでは使わない**（公式明記） [1]         | Microsoft Learnでは**断言しない**（Anthropic文書参照） [2] |
| 処理場所      | 原則 **顧客指定 geography 内**（例外あり、Global/DataZone等）[1] | **世界中で処理され得る**（地域外含む） [2]          |
| モデルが覚える？ | **ステートレス**（公式明記） [1]                      | 保存・スクリーニング等はAnthropic文書参照 [2]       |

---

## チェックリスト（導入前に確認すべきポイント）

1. 利用予定のモデルが**Azure Direct Models**かどうかを確認する  
2. **処理場所の前提**（geography / Global / DataZone 等）が設計・監査要件と合致するか確認する  
3. プロンプトや出力が**学習利用されないことの根拠**（公式文言や契約）を説明可能か  
4. Files / vector store / Threads など**保存が発生する機能の有無と保存条件**を理解し説明可能か  

### Azure AI Foundry のモデル一覧とリージョン対応

モデル一覧とリージョン対応は以下のURLで確認できます。  
https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability  

日本リージョンでは使えるモデルが少なく、処理場所にこだわると利用可能モデルがさらに限られる点にご注意ください。

---

## 「このモデルは Azure Direct Models なの？」を確認する方法

実務的には以下いずれかの方法が有効です。  

- Foundryのモデルカタログで「Direct from Azure」などの絞り込みを行う（UIは変更される可能性あり）  
- 公式ドキュメントで「sold directly by Azure」に該当するか確認する  

参考：  
https://learn.microsoft.com/ja-jp/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic  

---

## FAQ

### Q. 「Foundry から呼べる」＝「Microsoft が全部面倒を見る」ではない？

FoundryのUIから利用できても、データ処理者がモデル提供者（例：Anthropic）であることがあります。  
Microsoft Learnのページで**processor（処理者）が誰か**を必ず確認してください。 [1][2]

### Q. Azure Direct Modelsは“絶対に”geography外で処理されない？

「地域外処理なし」と断言するのは危険です。  
公式では「顧客指定のgeography内が原則」かつ「GlobalやDataZoneのデプロイ種別では他地域で処理される可能性がある」と説明しています。  

> Prompts and responses are processed within the customer-specified geography (unless you are using a Global or DataZone deployment type), but may be processed between regions within the geography for operational purposes...  
> For any deployment type labeled 'Global,' prompts and responses may be processed in any geography where the relevant Azure Direct Model is deployed...  
> For any deployment type labeled 'DataZone,' prompts and responses may be processed in any geography within the specified data zone...

（引用：公式ドキュメント [1]）

### Q. 「学習に使われない」ことのメリットは？

企業利用においては説明責任が最も効きます。  
監査や規制、顧客要件に対し、「学習に使われない」ことを**公式文言**で説明できるかで選定の難易度が変わります。  

> are NOT used to train any generative AI foundation models without your permission or instruction  
> Customer Data, Prompts, and Completions are NOT used to improve Microsoft or third-party products or services without your explicit permission or instruction.  
> The models are stateless: no prompts or completions are stored in the model. Additionally, prompts and completions are not used to train, retrain, or improve the base models.

（引用：公式ドキュメント [1]）

### Q. アップロードしたファイルの扱いは？

Azure Direct Modelsではアップロードデータは特定の機能（Files / vector store / Stored completions / Responses API / Threadsなど）によりサービス内のFoundryリソース（顧客指定geography）に保存される場合があります。  
保存データはAES-256等で暗号化され、顧客による削除が可能です。  
また、不正利用監視のためにサンプルが人によるレビュー用に保管されることもあります。  
いかなる場合でも長期保存や他顧客との共有は行われません。  

（詳細：公式ドキュメント [1]）

---

## 最後に

Foundry利用時のデータ取り扱いの大枠は、「モデル名」より前に**“Azure Direct Models かどうか”**で決まります。  
迷ったらMicrosoft Learnのデータ・プライバシーページを根拠に、組織のポリシーに合うモデルを選ぶのが安全です。  


誤りや改善点があればコメントいただけると助かります。

---

## 参考リンク（公式）

- Azure Direct Models のデータ・プライバシー：  
  https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic  
- Claude models のデータ・プライバシー：  
https://learn.microsoft.com/ja-jp/azure/ai-foundry/responsible-ai/claude-models/data-privacy?view=foundry 


[1] Azure Direct Models データ・プライバシー:  
https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy?view=foundry-classic  

[2] Claude models データ・プライバシー:  
https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/claude-models/data-privacy?view=foundry-classic  

Models sold directly by Azure：  
https://learn.microsoft.com/ja-jp/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic  

