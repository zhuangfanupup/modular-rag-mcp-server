# QA 涓撻」娴嬭瘯璁″垝 鈥?Modular RAG MCP Server

> **鐗堟湰**: 1.0  
> **鏃ユ湡**: 2025-02-25  
> **娴嬭瘯鑼冨洿**: 绯荤粺鍔熻兘楠岃瘉銆丏ashboard UI 浜や簰銆丆LI 鑴氭湰銆丳rovider 鍒囨崲銆佹暟鎹敓鍛藉懆鏈熴€佸閿欓檷绾? 
> **娴嬭瘯鐜**: Windows, Python 3.11+, 铏氭嫙鐜 `.venv`  
> **褰撳墠閰嶇疆**: Azure 鍏ㄥ妗?(LLM/Embedding/Vision LLM 鍧囦负 Azure OpenAI)

---

## 鐩綍

- [A. Dashboard 鈥?Overview 椤甸潰](#a-dashboard--overview-椤甸潰)
- [B. Dashboard 鈥?Data Browser 椤甸潰](#b-dashboard--data-browser-椤甸潰)
- [C. Dashboard 鈥?Ingestion Manager 椤甸潰](#c-dashboard--ingestion-manager-椤甸潰)
- [D. Dashboard 鈥?Ingestion Traces 椤甸潰](#d-dashboard--ingestion-traces-椤甸潰)
- [E. Dashboard 鈥?Query Traces 椤甸潰](#e-dashboard--query-traces-椤甸潰)
- [F. Dashboard 鈥?Evaluation Panel 椤甸潰](#f-dashboard--evaluation-panel-椤甸潰)
- [G. CLI 鈥?鏁版嵁鎽勫彇 (ingest.py)](#g-cli--鏁版嵁鎽勫彇-ingestpy)
- [H. CLI 鈥?鏌ヨ (query.py)](#h-cli--鏌ヨ-querypy)
- [I. CLI 鈥?璇勪及 (evaluate.py)](#i-cli--璇勪及-evaluatepy)
- [J. MCP Server 鍗忚浜や簰](#j-mcp-server-鍗忚浜や簰)
- [K. Provider 鍒囨崲 鈥?DeepSeek LLM](#k-provider-鍒囨崲--deepseek-llm)
- [L. Provider 鍒囨崲 鈥?Reranker 妯″紡](#l-provider-鍒囨崲--reranker-妯″紡)
- [M. 閰嶇疆鍙樻洿涓庡閿橾(#m-閰嶇疆鍙樻洿涓庡閿?
- [N. 鏁版嵁鐢熷懡鍛ㄦ湡闂幆](#n-鏁版嵁鐢熷懡鍛ㄦ湡闂幆)
- [O. 鏂囨。鏇挎崲涓庡鍦烘櫙楠岃瘉](#o-鏂囨。鏇挎崲涓庡鍦烘櫙楠岃瘉)

---

## 绯荤粺鐘舵€佸畾涔?

娴嬭瘯鐢ㄤ緥鐨?鐘舵€?鍒楁爣鏄庤娴嬭瘯闇€瑕佺郴缁熷浜庡摢涓姸鎬併€傛祴璇曡剼鏈嚜鍔ㄦ娴嬪綋鍓嶇姸鎬佸苟鍒囨崲銆?

| 鐘舵€佸€?| 鍚箟 | 濡備綍鍒拌揪 |
|--------|------|---------|
| `Empty` | 鍏ㄧ┖锛氭棤鏁版嵁銆佹棤 Trace | `qa_bootstrap.py` 涓?clear 姝ラ锛屾垨 Dashboard Clear All Data |
| `Baseline` | 鏍囧噯鏁版嵁锛歞efault 闆嗗悎(simple.pdf + with_images.pdf)銆乼est_col 闆嗗悎(complex_technical_doc.pdf)銆佹湁 Trace | `python .github/skills/qa-tester/scripts/qa_bootstrap.py` |
| `DeepSeek` | Baseline + LLM 鍒囧埌 DeepSeek + Vision 鍏抽棴 | `qa_config.py apply deepseek`锛堥渶 test_credentials.yaml锛?|
| `Rerank_LLM` | Baseline + LLM 閲嶆帓鍚敤 | `qa_config.py apply rerank_llm` |
| `NoVision` | Baseline + Vision LLM 鍏抽棴 | `qa_config.py apply no_vision` |
| `InvalidKey` | Baseline + LLM API Key 鏃犳晥 | `qa_config.py apply invalid_llm_key` |
| `InvalidEmbedKey` | Baseline + Embedding API Key 鏃犳晥 | `qa_config.py apply invalid_embed_key` |
| `Any` | 浠绘剰鐘舵€佸潎鍙?| 鏃犻渶鍒囨崲 |

> 鎵€鏈?config 绫荤姸鎬侊紙DeepSeek/Rerank_LLM 绛夛級娴嬪畬鍚庢墽琛?`qa_config.py restore` 鍥炲埌 Baseline銆?

---

## A. Dashboard 鈥?Overview 椤甸潰

> 鍚姩鏂瑰紡: `python scripts/start_dashboard.py` 鈫?娴忚鍣ㄦ墦寮€ `http://localhost:8501`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| A-01 | Overview 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 鎵撳紑娴忚鍣ㄨ闂?`http://localhost:8501` | 椤甸潰鏍囬鏄剧ず"馃搳 System Overview"锛屾棤鎶ラ敊 |
| A-02 | 缁勪欢閰嶇疆鍗＄墖灞曠ず姝ｇ‘ | Baseline | 1. 鏌ョ湅"馃敡 Component Configuration"鍖哄煙 | 鏄剧ず LLM(azure/gpt-4o)銆丒mbedding(azure/ada-002)銆乂ector Store(chroma)銆丷etrieval銆丷eranker(none)銆乂ision LLM(azure/gpt-4o)銆両ngestion 鍏?7 寮犲崱鐗囷紝provider 鍜?model 涓?settings.yaml 涓€鑷?|
| A-03 | 缁勪欢鍗＄墖璇︽儏灞曞紑 | Baseline | 1. 鐐瑰嚮浠绘剰缁勪欢鍗＄墖鐨?Details"灞曞紑 | 灞曠ず璇ョ粍浠剁殑棰濆閰嶇疆淇℃伅锛堝 LLM 鍗＄墖灞曠ず temperature銆乵ax_tokens 绛夛級 |
| A-04 | 闆嗗悎缁熻鏄剧ず姝ｇ‘ | Baseline | 1. 鏌ョ湅"馃摝 Data Assets"鍖哄煙 | 鏄剧ず default 闆嗗悎鐨?chunk 鏁伴噺锛屾暟瀛?> 0 |
| A-05 | 绌烘暟鎹簱鏃剁殑闆嗗悎缁熻 | Empty | 1. 鏌ョ湅"馃摝 Data Assets"鍖哄煙 | 鏄剧ず "鈿狅笍 No collections found or ChromaDB unavailable" 璀﹀憡淇℃伅 |
| A-06 | Trace 缁熻鏄剧ず姝ｇ‘ | Baseline | 1. 鏌ョ湅 Trace 缁熻鍖哄煙 | 鏄剧ず "Total traces" 鏁板瓧 > 0 |
| A-07 | 鏃?Trace 鏃剁殑绌虹姸鎬?| Empty | 1. 鏌ョ湅 Trace 缁熻鍖哄煙 | 鏄剧ず "No traces recorded yet" 淇℃伅鎻愮ず |
| A-08 | 淇敼 settings.yaml 鍚庡埛鏂?| Baseline | 1. 鎵嬪姩缂栬緫 `settings.yaml` 灏?`llm.model` 鏀逛负 `gpt-4`<br>2. 鍒锋柊娴忚鍣ㄩ〉闈?| LLM 鍗＄墖鏇存柊鏄剧ず gpt-4锛堝洜 ConfigService 閲嶆柊璇诲彇閰嶇疆锛夛紝鏀瑰洖 gpt-4o 鍚庡啀鍒锋柊鎭㈠ |

---

## B. Dashboard 鈥?Data Browser 椤甸潰

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| B-01 | Data Browser 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 宸︿晶瀵艰埅鐐瑰嚮"Data Browser" | 椤甸潰鏄剧ず闆嗗悎閫夋嫨涓嬫媺妗嗭紝鏃犳姤閿?|
| B-02 | 闆嗗悎涓嬫媺妗嗛€夐」姝ｇ‘ | Baseline | 1. 鐐瑰嚮闆嗗悎涓嬫媺妗?| 涓嬫媺鍒楄〃鍖呭惈 default 鍜?test_col 涓や釜閫夐」 |
| B-03 | 閫夋嫨闆嗗悎鍚庢枃妗ｅ垪琛ㄥ睍绀?| Baseline | 1. 涓嬫媺妗嗛€夋嫨 "default" | 椤甸潰灞曠ず 2 涓枃妗ｆ潯鐩紙simple.pdf 鍜?with_images.pdf锛夛紝姣忎釜鏄剧ず鏂囦欢鍚嶃€乧hunk 鏁般€佸浘鐗囨暟銆俿imple.pdf 鍥剧墖鏁?0锛寃ith_images.pdf 鍥剧墖鏁扳墺1 |
| B-04 | 灞曞紑鏂囨。鏌ョ湅 Chunk 璇︽儏 | Baseline | 1. 鐐瑰嚮 simple.pdf 鏂囨。鐨勫睍寮€绠ご | 灞曠ず simple.pdf 鐨勬墍鏈?Chunk锛堟暟閲?鈮?1锛夛紝姣忎釜 Chunk 鏄剧ず鏂囨湰鍐呭锛堝彧璇绘枃鏈锛屽簲鍚?"Sample Document" 鐩稿叧鍐呭锛夊拰 Metadata 灞曞紑鎸夐挳 |
| B-05 | 鏌ョ湅 Chunk Metadata | Baseline | 1. 灞曞紑 simple.pdf 鐨勭涓€涓?Chunk<br>2. 鐐瑰嚮"馃搵 Metadata"灞曞紑 | 鏄剧ず JSON 鏍煎紡鐨?metadata锛屽寘鍚?source 瀛楁锛堝€煎惈 "simple.pdf"锛夈€乨oc_hash锛圫HA256 鍝堝笇锛夈€乼itle銆乼ags 绛夊瓧娈?|
| B-06 | 鏌ョ湅鍏宠仈鍥剧墖棰勮 | Baseline | 1. 灞曞紑鍚浘鐗囩殑鏂囨。(with_images.pdf)<br>2. 鏌ョ湅鍥剧墖棰勮鍖哄煙 | 椤甸潰鏄剧ず鍥剧墖缂╃暐鍥撅紙鏈€澶?4 鍒楃綉鏍兼帓鍒楋級 |
| B-07 | 鍒囨崲闆嗗悎鍚庢枃妗ｅ垪琛ㄥ埛鏂?| Baseline | 1. 涓嬫媺妗嗕粠 default 鍒囨崲鍒?test_col | 鏂囨。鍒楄〃鍒锋柊锛屾樉绀?test_col 闆嗗悎鐨勬枃妗ｏ紙鍖呭惈 complex_technical_doc.pdf锛夛紝涓嶅啀鏄剧ず default 鐨?simple.pdf/with_images.pdf |
| B-08 | 绌洪泦鍚堢殑鏄剧ず | Empty | 1. 閫夋嫨绌洪泦鍚?| 鏄剧ず "No documents found" 淇℃伅鎻愮ず |
| B-09 | Clear All Data 鈥?纭娴佺▼ | Baseline | 1. 灞曞紑"鈿狅笍 Danger Zone"<br>2. 鐐瑰嚮"馃棏锔?Clear All Data"<br>3. 瑙傚療纭瀵硅瘽妗?| 鍑虹幇"鉁?Yes, delete everything"鍜?鉂?Cancel"涓や釜鎸夐挳锛屼笉浼氱洿鎺ュ垹闄?|
| B-10 | Clear All Data 鈥?鍙栨秷鎿嶄綔 | Baseline | 1. 鐐瑰嚮"鉂?Cancel" | 瀵硅瘽妗嗘秷澶憋紝鏁版嵁鏈鍒犻櫎锛屾枃妗ｅ垪琛ㄤ笉鍙?|
| B-11 | Clear All Data 鈥?纭鍒犻櫎 | Baseline | 1. 鐐瑰嚮"鉁?Yes, delete everything" | 鏄剧ず鎴愬姛鎻愮ず锛岄〉闈㈠埛鏂板悗鏂囨。鍒楄〃涓虹┖锛屾墍鏈夐泦鍚堟暟鎹竻绌?|
| B-12 | Clear All Data 鍚庨獙璇佸悇瀛樺偍 | Empty | 1. 鍒囨崲鍒?Overview 椤甸潰鏌ョ湅闆嗗悎缁熻<br>2. 妫€鏌?`data/db/chroma` 鐩綍<br>3. 妫€鏌?`data/images` 鐩綍<br>4. 妫€鏌?`logs/traces.jsonl` | Overview 鏄剧ず鏃犻泦鍚堬紱Chroma 鐩綍琚竻绌烘垨闆嗗悎涓虹┖锛汭mages 鐩綍琚竻绌猴紱traces.jsonl 琚竻绌?|

---

## C. Dashboard 鈥?Ingestion Manager 椤甸潰

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| C-01 | Ingestion Manager 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 宸︿晶瀵艰埅鐐瑰嚮"Ingestion Manager" | 椤甸潰鏄剧ず鏂囦欢涓婁紶鍖哄煙鍜岄泦鍚堣緭鍏ユ锛屾棤鎶ラ敊 |
| C-02 | 涓婁紶 PDF 鏂囦欢骞舵憚鍙?| Baseline | 1. 鐐瑰嚮鏂囦欢涓婁紶鍖哄煙锛岄€夋嫨 `tests/fixtures/sample_documents/simple.pdf`<br>2. 闆嗗悎鍚嶄繚鎸?"default"<br>3. 鐐瑰嚮"馃殌 Start Ingestion" | 杩涘害鏉′粠 0% 鎺ㄨ繘锛屼緷娆℃樉绀?integrity鈫抣oad鈫抯plit鈫抰ransform鈫抏mbed鈫抲psert 鍚勯樁娈碉紝鏈€缁堟樉绀烘垚鍔熸彁绀?|
| C-03 | 鎽勫彇瀹屾垚鍚庢枃妗ｅ嚭鐜板湪鍒楄〃 | Baseline | 1. 鏌ョ湅涓嬫柟鏂囨。鍒楄〃 | 鍒楄〃涓嚭鐜?simple.pdf 鏉＄洰锛屾樉绀?chunk 鏁伴噺 > 0 |
| C-04 | 鎽勫彇鍚浘鐗囩殑 PDF | Baseline | 1. 涓婁紶 `tests/fixtures/sample_documents/with_images.pdf`<br>2. 鐐瑰嚮"馃殌 Start Ingestion" | 杩涘害鏉℃甯告帹杩涳紝Transform 闃舵澶勭悊鍥剧墖 captioning锛屾渶缁堟垚鍔熴€傛枃妗ｅ垪琛ㄦ樉绀哄浘鐗囨暟 > 0 |
| C-05 | 鎽勫彇鍒拌嚜瀹氫箟闆嗗悎 | Baseline | 1. 涓婁紶 `tests/fixtures/sample_documents/chinese_technical_doc.pdf`<br>2. 闆嗗悎鍚嶈緭鍏?"my_collection"<br>3. 鐐瑰嚮"馃殌 Start Ingestion" | 鎽勫彇鎴愬姛锛屾枃妗ｅ綊鍏?my_collection 闆嗗悎銆傚垏鎹㈠埌 Data Browser 鍙湅鍒?my_collection 闆嗗悎锛屽叾涓寘鍚?chinese_technical_doc.pdf |
| C-06 | 閲嶅鎽勫彇鍚屼竴鏂囦欢锛堝箓绛夋€э級 | Baseline | 1. 鍐嶆涓婁紶 simple.pdf 鍒?default 闆嗗悎<br>2. 鐐瑰嚮"馃殌 Start Ingestion" | 绯荤粺妫€娴嬪埌鏂囦欢宸插鐞嗭紙SHA256 鍖归厤锛夛紝璺宠繃澶勭悊鎴栧揩閫熷畬鎴愶紝涓嶄骇鐢熼噸澶?Chunk |
| C-07 | 寮哄埗閲嶆柊鎽勫彇 | Baseline | 1. 鍦ㄦ枃妗ｅ垪琛ㄤ腑鍒犻櫎 simple.pdf<br>2. 鍐嶆涓婁紶 simple.pdf 骞舵憚鍙?| 閲嶆柊澶勭悊鍏ㄦ祦绋嬶紝Chunk 閲嶆柊鐢熸垚 |
| C-08 | 鍒犻櫎鍗曚釜鏂囨。 | Baseline | 1. 鍦?default 闆嗗悎涓壘鍒?simple.pdf 鏉＄洰<br>2. 鐐瑰嚮 simple.pdf 鏃佺殑"馃棏锔?Delete"鎸夐挳 | simple.pdf 浠庡垪琛ㄦ秷澶憋紝鏄剧ず鎴愬姛鎻愮ず銆傝法 4 涓瓨鍌紙Chroma銆丅M25銆両mages銆丗ileIntegrity锛夊潎宸叉竻鐞?|
| C-09 | 鍒犻櫎鏂囨。鍚庢煡璇㈤獙璇?| Baseline | 1. 鎵挎帴 C-08 鍒犻櫎 simple.pdf 鍚?br>2. 鎵ц `python scripts/query.py --query "Sample Document PDF loader" --verbose` | 鏌ヨ缁撴灉涓嶅啀鍖呭惈鏉ユ簮涓?simple.pdf 鐨?Chunk锛宻ource_file 瀛楁涓棤 simple.pdf |
| C-10 | 涓婁紶闈?PDF 鏂囦欢 | Baseline | 1. 涓婁紶 `tests/fixtures/sample_documents/sample.txt`<br>2. 闆嗗悎鍚嶄繚鎸?"default"<br>3. 鐐瑰嚮"馃殌 Start Ingestion" | 鏂囦欢涓婁紶缁勪欢鎺ュ彈 txt锛堟敮鎸?pdf/txt/md/docx锛夈€傛憚鍙栨祦绋嬫甯稿鐞?sample.txt锛岀敓鎴?Chunk 骞跺瓨鍏?default 闆嗗悎 |
| C-11 | 涓嶉€夋嫨鏂囦欢鐩存帴鐐瑰嚮鎽勫彇 | Baseline | 1. 涓嶄笂浼犱换浣曟枃浠?br>2. 瑙傚療鏄惁鏈?馃殌 Start Ingestion"鎸夐挳 | 鎸夐挳涓嶆樉绀猴紙浠呭湪鏂囦欢涓婁紶鍚庡嚭鐜帮級锛屾棤娉曡鎿嶄綔 |
| C-12 | 鎽勫彇澶у瀷 PDF锛堟€ц兘瑙傚療锛?| Baseline | 1. 涓婁紶 `tests/fixtures/sample_documents/chinese_long_doc.pdf`锛?0+ 椤典腑鏂囬暱鏂囨。锛?br>2. 闆嗗悎鍚嶄繚鎸?"default"<br>3. 鐐瑰嚮"馃殌 Start Ingestion" | 杩涘害鏉℃甯告帹杩涳紝鍚勯樁娈佃€楁椂鍚堢悊锛圱ransform 鍙兘杈冩參鍥?LLM 璋冪敤锛?0+ 椤甸鏈?Split 鐢熸垚杈冨 Chunk锛夛紝鏈€缁堝畬鎴愭棤瓒呮椂 |
| C-13 | 鎽勫彇杩囩▼涓殑闃舵杩涘害灞曠ず | Baseline | 1. 涓婁紶 `tests/fixtures/sample_documents/chinese_technical_doc.pdf`锛垀8 椤碉紝鍙骇鐢熷涓?Chunk锛?br>2. 闆嗗悎鍚嶄繚鎸?"default"锛岀偣鍑?馃殌 Start Ingestion"<br>3. 瑙傚療杩涘害鏉?| 杩涘害鏉℃枃瀛椾緷娆℃樉绀哄悇闃舵鍚嶇О锛堝"transform 2/5"锛夛紝鐧惧垎姣旈€掑 |

---

## D. Dashboard 鈥?Ingestion Traces 椤甸潰

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| D-01 | Ingestion Traces 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 宸︿晶瀵艰埅鐐瑰嚮"Ingestion Traces" | 椤甸潰鏄剧ず鎽勫彇鍘嗗彶鍒楄〃锛屾寜鏃堕棿鍊掑簭鎺掑垪 |
| D-02 | Trace 鍒楄〃鏉＄洰淇℃伅瀹屾暣 | Baseline | 1. 鏌ョ湅鍒楄〃涓殑姣忎釜鏉＄洰 | 姣忔潯鏄剧ず锛氭枃浠跺悕銆佹€昏€楁椂锛堢锛夈€佹椂闂存埑 |
| D-03 | 灞曞紑鍗曟潯 Trace 鏌ョ湅姒傝鎸囨爣 | Baseline | 1. 鐐瑰嚮 with_images.pdf 瀵瑰簲鐨?Trace 灞曞紑绠ご锛堝洜鍚浘鐗囷紝鎸囨爣鏇翠赴瀵岋級 | 鏄剧ず 5 涓寚鏍囧崱鐗囷細Doc Length銆丆hunks銆両mages锛堚墺 1锛夈€乂ectors銆乀otal Time |
| D-04 | 鏌ョ湅鑰楁椂鐎戝竷鍥?| Baseline | 1. 鏌ョ湅鐎戝竷鍥惧尯鍩?| 姘村钩鏉″舰鍥炬樉绀?load/split/transform/embed/upsert 鍚勯樁娈电殑鑰楁椂鍒嗗竷锛岄樁娈靛悕鍜岃€楁椂(ms)鍙 |
| D-05 | Load 闃舵 Tab 璇︽儏 | Baseline | 1. 灞曞紑 simple.pdf 鐨?Trace<br>2. 鐐瑰嚮"馃搫 Load"Tab | 鏄剧ず Doc ID銆乀ext Length锛? 0锛夈€両mages 鏁伴噺锛坰imple.pdf 涓?0锛夋寚鏍囷紝浠ュ強 Raw Text 棰勮锛堝簲鍚?"Sample Document" 鏂囨湰锛?|
| D-06 | Split 闃舵 Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"鉁傦笍 Split"Tab | 鏄剧ず Chunks 鏁伴噺鍜?Avg Size 鎸囨爣锛屾瘡涓?Chunk 鍙睍寮€鏌ョ湅鏂囨湰鍐呭 |
| D-07 | Transform 闃舵 Tab 璇︽儏 | Baseline | 1. 灞曞紑 with_images.pdf 鐨?Trace锛堝洜鍚浘鐗囷紝鍙獙璇?captioning锛?br>2. 鐐瑰嚮"馃攧 Transform"Tab | 鏄剧ず Refined/Enriched/Captioned 鏁伴噺鎸囨爣锛圕aptioned 鈮?1锛夛紝姣忎釜 Chunk 鍙睍寮€鏌ョ湅 metadata (title/tags/summary) 鍜?before/after 鏂囨湰瀵规瘮锛堝弻鍒楀竷灞€锛?|
| D-08 | Embed 闃舵 Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃敘 Embed"Tab | 鏄剧ず Dense Vectors銆丏imension銆丼parse Docs銆丮ethod 鎸囨爣锛屼互鍙?Dense/Sparse 缂栫爜鏁版嵁琛ㄦ牸 |
| D-09 | Upsert 闃舵 Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃捑 Upsert"Tab | 鏄剧ず Dense Vectors銆丼parse BM25銆両mages 瀛樺偍鏁伴噺锛屼互鍙婂瓨鍌ㄨ鎯呭睍寮€ |
| D-10 | 鏃?Trace 鏃剁殑绌虹姸鎬?| Empty | 1. 鎵撳紑 Ingestion Traces 椤甸潰 | 鏄剧ず "No ingestion traces recorded yet" 淇℃伅鎻愮ず |
| D-11 | 澶辫触鐨勬憚鍙?Trace 灞曠ず | InvalidKey | 1. 鏌ョ湅澶辫触鐨?Trace | Trace 鏉＄洰鏄剧ず澶辫触鐘舵€侊紝灞曞紑鍚庡搴旈樁娈垫樉绀虹孩鑹查敊璇俊鎭?|
| D-12 | 澶氭鎽勫彇鐨?Trace 鎺掑簭 | Baseline | 1. 鏌ョ湅 Trace 鍒楄〃 | 鏈€鏂扮殑鎽勫彇璁板綍鎺掑湪鏈€鍓嶉潰锛堝€掑簭锛夛紝鏃堕棿鎴抽€掑噺 |

---

## E. Dashboard 鈥?Query Traces 椤甸潰

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| E-01 | Query Traces 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 宸︿晶瀵艰埅鐐瑰嚮"Query Traces" | 椤甸潰鏄剧ず鏌ヨ鍘嗗彶鍒楄〃锛屾湁鍏抽敭璇嶆悳绱㈡ |
| E-02 | 鍏抽敭璇嶆悳绱㈣繃婊?| Baseline | 1. 鍦ㄦ悳绱㈡杈撳叆 "hybrid search"锛圔aseline 寤虹珛鏃?qa_bootstrap.py 浼氭墽琛屾鏌ヨ锛?br>2. 瑙傚療鍒楄〃鍙樺寲 | 浠呮樉绀?query 鍖呭惈 "hybrid search" 鐨勬煡璇?Trace锛屽叾浠栨煡璇?Trace 琚繃婊ゆ帀 |
| E-03 | 灞曞紑鍗曟潯 Trace 鏌ョ湅姒傝鎸囨爣 | Baseline | 1. 灞曞紑鏌愭潯 Trace | 鏄剧ず 5 涓寚鏍囧崱鐗囷細Dense Hits銆丼parse Hits銆丗used銆丄fter Rerank銆乀otal Time |
| E-04 | 鏌ョ湅鏌ヨ鑰楁椂鐎戝竷鍥?| Baseline | 1. 鏌ョ湅鐎戝竷鍥?| 鏄剧ず query_processing/dense/sparse/fusion/rerank 鍚勯樁娈佃€楁椂 |
| E-05 | Query Processing Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃敜 Query Processing"Tab | 鏄剧ず鍘熷 Query銆丮ethod銆佹彁鍙栫殑鍏抽敭璇嶅垪琛?|
| E-06 | Dense Retrieval Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃煢 Dense"Tab | 鏄剧ず Method銆丳rovider銆丷esults 鏁伴噺銆乀op-K 璁剧疆锛屼互鍙婃寜鍒嗘暟鐫€鑹茬殑 Chunk 鍒楄〃锛堭煙⑩墺0.8/馃煛鈮?.5/馃敶<0.5锛?|
| E-07 | Sparse Retrieval Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃煥 Sparse"Tab | 鏄剧ず Method (BM25)銆並eywords銆丷esults 鏁伴噺銆乀op-K锛屼互鍙?Chunk 鍒楄〃鍜屽垎鏁?|
| E-08 | Fusion Tab 璇︽儏 | Baseline | 1. 鐐瑰嚮"馃煩 Fusion"Tab | 鏄剧ず Method (RRF)銆両nput Lists 鏁伴噺銆丗used Results 鏁伴噺锛屼互鍙婅瀺鍚堝悗鐨勭粺涓€鎺掑悕鍒楄〃 |
| E-09 | Rerank Tab 鈥?鏈惎鐢ㄦ儏鍐?| Baseline | 1. 鐐瑰嚮"馃煪 Rerank"Tab | 鏄剧ず "Rerank skipped (not enabled)" 淇℃伅鎻愮ず |
| E-10 | Dense vs Sparse 缁撴灉瀵规瘮 | Baseline | 1. 鍒嗗埆鏌ョ湅 Dense 鍜?Sparse Tab | 鍙姣斾袱璺彫鍥炵殑涓嶅悓 Chunk ID銆佹枃妗ｆ潵婧愩€佸垎鏁帮紝瑙傚療浜掕ˉ鎬?|
| E-11 | Ragas Evaluate 鎸夐挳鍔熻兘 | Baseline | 1. 灞曞紑 query 涓?"What is hybrid search" 鐨?Trace锛堟垨鏈€鏂颁竴鏉?Trace锛?br>2. 鐐瑰嚮"馃搹 Ragas Evaluate"鎸夐挳<br>3. 绛夊緟 loading spinner 瀹屾垚 | 鏄剧ず Ragas 璇勪及缁撴灉鎸囨爣鍗＄墖锛坒aithfulness銆乤nswer_relevancy銆乧ontext_precision锛夛紝鍒嗘暟鍦?0-1 涔嬮棿 |
| E-12 | Ragas Evaluate 澶辫触澶勭悊 | InvalidKey | 1. 灏?settings.yaml 鐨?llm api_key 鏀逛负鏃犳晥鍊?br>2. 鐐瑰嚮"馃搹 Ragas Evaluate" | 鏄剧ず绾㈣壊閿欒鎻愮ず锛屼笉宕╂簝 |
| E-13 | 鏃犳煡璇?Trace 鏃剁殑绌虹姸鎬?| Empty | 1. 鎵撳紑 Query Traces 椤甸潰 | 鏄剧ず "No query traces recorded yet" 淇℃伅鎻愮ず |

---

## F. Dashboard 鈥?Evaluation Panel 椤甸潰

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| F-01 | Evaluation Panel 椤甸潰姝ｅ父鍔犺浇 | Baseline | 1. 宸︿晶瀵艰埅鐐瑰嚮"Evaluation Panel" | 椤甸潰鏄剧ず璇勪及鍚庣閫夋嫨銆佸弬鏁伴厤缃尯鍩?|
| F-02 | Ragas Evaluator 杩愯 | Baseline | 1. Backend 閫夋嫨 "ragas"<br>2. Top-K 淇濇寔 10<br>3. Golden Path 淇濇寔榛樿<br>4. 鐐瑰嚮"鈻讹笍 Run Evaluation" | 璇勪及杩愯锛堝彲鑳借緝鎱級锛屾樉绀?faithfulness銆乤nswer_relevancy銆乧ontext_precision 鎸囨爣 |
| F-03 | 姣忔潯鏌ヨ鐨勮缁嗙粨鏋?| Baseline | 1. 瀹屾垚涓€娆?Ragas 璇勪及鍚庢煡鐪?per-query 缁撴灉鍖哄煙 | 姣忔潯 golden test set query 灞曞紑鏄剧ず锛氭绱㈠埌鐨?Chunk ID銆佺敓鎴愮殑绛旀銆佸悇椤?Ragas 鎸囨爣鍒嗘暟 |
| F-04 | Golden Test Set 璺緞鏃犳晥 | Baseline | 1. 灏?Golden Path 鏀逛负 `tests/fixtures/nonexistent_test_set.json`<br>2. 瑙傚療"鈻讹笍 Run Evaluation"鎸夐挳鐘舵€?| 鎸夐挳鍙樹负绂佺敤鐘舵€侊紙disabled锛夛紝鏄剧ず璺緞鏃犳晥璀﹀憡 |
| F-05 | 璇勪及鍘嗗彶璁板綍灞曠ず | Baseline | 1. 婊氬姩鍒伴〉闈㈠簳閮ㄧ殑 History 鍖哄煙 | 鏄剧ず鍘嗗彶璇勪及杩愯鐨勮〃鏍硷紙鏈€杩?10 鏉★級锛屽寘鍚椂闂村拰鍚勯」鎸囨爣 |
| F-06 | 鎸囧畾闆嗗悎鍚嶈瘎浼?| Baseline | 1. 鍏堝湪 Ingestion Manager 涓婁紶 `tests/fixtures/sample_documents/chinese_technical_doc.pdf` 鍒伴泦鍚?"my_collection" 骞跺畬鎴愭憚鍙?br>2. 鍒囨崲鍒?Evaluation Panel锛孋ollection 杈撳叆 "my_collection"<br>3. 杩愯璇勪及 | 璇勪及浠呴拡瀵?my_collection 闆嗗悎鐨勬暟鎹繘琛屾绱?|
| F-07 | 绌虹煡璇嗗簱杩愯璇勪及 | Empty | 1. 鐐瑰嚮杩愯璇勪及 | 璇勪及瀹屾垚浣嗗悇椤规寚鏍囧亸浣庢垨涓?0锛屼笉宕╂簝 |

---

## G. CLI 鈥?鏁版嵁鎽勫彇 (ingest.py)

> 鍛戒护鏍煎紡: `python scripts/ingest.py --path <璺緞> [閫夐」]`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| G-01 | 鎽勫彇鍗曚釜 PDF 鏂囦欢 | Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf` | 鎺у埗鍙拌緭鍑哄悇闃舵澶勭悊淇℃伅锛屾渶缁堟樉绀烘憚鍙栨垚鍔燂紝exit code=0 |
| G-02 | 鎽勫彇鏁翠釜鐩綍 | Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/` | 鑷姩鍙戠幇鐩綍涓嬫墍鏈?.pdf 鏂囦欢锛岄€愪釜澶勭悊锛屾渶缁堟樉绀烘憚鍙栨眹鎬伙紙鎴愬姛鏁?澶辫触鏁帮級 |
| G-03 | 鎸囧畾闆嗗悎鍚嶆憚鍙?| Baseline | 1. 鎵ц `python scripts/ingest.py --path simple.pdf --collection test_col` | 鏂囦欢鎽勫彇鍒?test_col 闆嗗悎锛屽彲鍦?Dashboard Data Browser 涓湅鍒?|
| G-04 | --dry-run 妯″紡 | Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/ --dry-run` | 浠呭垪鍑哄皢瑕佸鐞嗙殑鏂囦欢鍒楄〃锛屼笉瀹為檯鎵ц鎽勫彇锛屾棤 API 璋冪敤 |
| G-05 | --force 寮哄埗閲嶆柊澶勭悊 | Baseline | 1. 鎵ц `python scripts/ingest.py --path simple.pdf --force` | 璺宠繃 SHA256 妫€鏌ワ紝寮哄埗閲嶆柊澶勭悊鍏ㄦ祦绋?|
| G-06 | 閲嶅鎽勫彇锛堟棤 --force锛?| Baseline | 1. 鎵ц `python scripts/ingest.py --path simple.pdf`锛堜笉鍔?--force锛?| 鎺у埗鍙版彁绀烘枃浠跺凡澶勭悊/璺宠繃锛屼笉浜х敓閲嶅 Chunk |
| G-07 | --verbose 璇︾粏杈撳嚭 | Baseline | 1. 鎵ц `python scripts/ingest.py --path simple.pdf --verbose` | 杈撳嚭 DEBUG 绾у埆鏃ュ織锛屽寘鍚悇闃舵璇︾粏淇℃伅 |
| G-08 | 鎸囧畾閰嶇疆鏂囦欢 | Baseline | 1. 鎵ц `python scripts/ingest.py --path simple.pdf --config config/settings_test.yaml` | 浣跨敤鎸囧畾閰嶇疆鏂囦欢鐨勮缃繘琛屾憚鍙?|
| G-09 | 璺緞涓嶅瓨鍦ㄦ椂鐨勬姤閿?| Any | 1. 鎵ц `python scripts/ingest.py --path /涓嶅瓨鍦ㄧ殑璺緞/abc.pdf` | 鎺у埗鍙版樉绀烘竻鏅扮殑 FileNotFoundError 淇℃伅锛宔xit code 鈮?0 |
| G-10 | 闈?PDF 鏂囦欢鐨勫鐞?| Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/`锛堣鐩綍鍖呭惈 .pdf 鍜?sample.txt锛?| 澶勭悊鎵€鏈?.pdf 鏂囦欢锛宻ample.txt 琚烦杩囷紙鎴栨湁瀵瑰簲 loader 澶勭悊锛夛紝杈撳嚭姹囨€绘樉绀哄 txt 鏂囦欢鐨勫鐞嗘儏鍐?|
| G-11 | 鎽勫彇鍚浘鐗?PDF 骞堕獙璇?captioning | Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/with_images.pdf --verbose` | 鏃ュ織涓樉绀?Image Captioning 澶勭悊淇℃伅锛岀敓鎴愮殑 caption 鏂囨湰鍙 |

---

## H. CLI 鈥?鏌ヨ (query.py)

> 鍛戒护鏍煎紡: `python scripts/query.py --query <鏌ヨ鏂囨湰> [閫夐」]`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| H-01 | 鍩烘湰涓枃鏌ヨ | Baseline | 1. 鎵ц `python scripts/query.py --query "Transformer 娉ㄦ剰鍔涙満鍒舵槸浠€涔?` | 杩斿洖鐩稿叧 Chunk 鍒楄〃锛孴op 缁撴灉涓簲鍖呭惈鏉ヨ嚜 complex_technical_doc.pdf 鎴?Baseline 涓惈鐩稿叧鍐呭鐨勬枃妗ｏ紝姣忎釜缁撴灉鏄剧ず鏂囨湰鐗囨銆佹潵婧愭枃浠躲€佸垎鏁?|
| H-02 | 鎸囧畾 top-k 鍙傛暟 | Baseline | 1. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation modular architecture" --top-k 3` | 鏈€澶氳繑鍥?3 鏉＄粨鏋滐紝缁撴灉涓簲鍖呭惈 complex_technical_doc.pdf 鐨?Chunk |
| H-03 | 鎸囧畾闆嗗悎鏌ヨ | Baseline | 1. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation" --collection test_col` | 浠呬粠 test_col 涓绱紝缁撴灉鍏ㄩ儴鏉ヨ嚜 complex_technical_doc.pdf锛屼笉娣峰叆 default 闆嗗悎鐨?simple.pdf/with_images.pdf |
| H-04 | --verbose 鏌ョ湅妫€绱㈣鎯?| Baseline | 1. 鎵ц `python scripts/query.py --query "娣峰悎妫€绱? --verbose` | 鍒嗗埆鏄剧ず Dense 鍙洖缁撴灉銆丼parse 鍙洖缁撴灉銆丗usion 铻嶅悎缁撴灉锛屽彲瀵规瘮鍚勮矾鍙洖 |
| H-05 | --no-rerank 绂佺敤閲嶆帓 | Rerank_LLM | 1. 鎵ц `python scripts/query.py --query "BM25 娣峰悎妫€绱㈣瀺鍚堢瓥鐣? --no-rerank --verbose` | 璺宠繃 Rerank 闃舵锛岀洿鎺ヨ繑鍥?RRF 铻嶅悎鍚庣殑缁撴灉锛孷erbose 涓棤 Rerank 姝ラ杈撳嚭 |
| H-06 | 绌烘煡璇㈢殑澶勭悊 | Any | 1. 鎵ц `python scripts/query.py --query ""` | 杩斿洖绌虹粨鏋滄垨鍚堢悊鐨勬彁绀轰俊鎭紝涓嶅穿婧?|
| H-07 | 瓒呴暱鏌ヨ鐨勫鐞?| Any | 1. 鎵ц `python scripts/query.py --query "Transformer 妯″瀷涓殑鑷敞鎰忓姏鏈哄埗濡備綍宸ヤ綔锛屽寘鎷?Multi-Head Attention 鍜?RoPE 浣嶇疆缂栫爜鐨勫師鐞嗭紝浠ュ強 KV Cache 浼樺寲绛栫暐銆傚悓鏃惰瑙ｉ噴 RAG 绯荤粺涓贩鍚堟绱㈢殑宸ヤ綔娴佺▼锛屽寘鎷?Dense Retrieval銆丅M25 Sparse Retrieval 鍜?RRF 铻嶅悎绠楁硶鐨勫叿浣撳疄鐜版柟寮忋€傝繕鏈?Cross-Encoder Reranker 鍜?LLM Reranker 鐨勫姣斿垎鏋愶紝浠ュ強鍦ㄧ敓浜х幆澧冧腑濡備綍閫夋嫨鍚堥€傜殑鍚戦噺鏁版嵁搴擄紙濡?ChromaDB銆丗AISS銆丮ilvus锛夋潵瀛樺偍鍜屾绱?Embedding 鍚戦噺銆傝璇︾粏璇存槑姣忎釜缁勪欢鐨勪紭缂虹偣鍜岄€傜敤鍦烘櫙銆?`锛堢害 250 瀛楃锛?| 姝ｅ父澶勭悊锛堟煡璇㈠彲鑳借鎴柇锛夛紝杩斿洖缁撴灉锛屼笉瓒呮椂涓嶅穿婧?|
| H-08 | 涓庢憚鍙栨枃妗ｅ唴瀹圭浉鍏崇殑鏌ヨ | Baseline | 1. 鎵ц `python scripts/query.py --query "Precision@5 Recall@10 performance benchmarks" --top-k 3`锛堣鍐呭瀛樺湪浜?complex_technical_doc.pdf 鐨勬€ц兘鍩哄噯绔犺妭锛?| Top-3 缁撴灉涓嚦灏戞湁 1 鏉℃潵鑷?complex_technical_doc.pdf锛屾枃鏈墖娈靛寘鍚?"Precision" 鎴?"benchmarks" 鐩稿叧鍐呭锛宻ource_file 瀛楁涓?complex_technical_doc.pdf |
| H-09 | 涓庢憚鍙栨枃妗ｆ棤鍏崇殑鏌ヨ | Baseline | 1. 鎵ц `python scripts/query.py --query "閲忓瓙鍔涘钖涘畾璋旀柟绋?` | 杩斿洖缁撴灉锛屼絾鍒嗘暟杈冧綆鎴栨棤缁撴灉锛岃涓哄悎鐞?|
| H-10 | 鏌ヨ鍚?Trace 璁板綍楠岃瘉 | Baseline | 1. 鎵ц `python scripts/query.py --query "What is hybrid search and how does it work"`<br>2. 鎵撳紑 Dashboard Query Traces 椤甸潰 | 鏈€鏂颁竴鏉?Trace 鐨?query 鏂囨湰鏄剧ず "What is hybrid search and how does it work"锛屾椂闂存埑涓哄垰鎵嶆墽琛岀殑鏃堕棿 |

---

## I. CLI 鈥?璇勪及 (evaluate.py)

> 鍛戒护鏍煎紡: `python scripts/evaluate.py [閫夐」]`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| I-01 | 榛樿璇勪及杩愯 | Baseline | 1. 鎵ц `python scripts/evaluate.py` | 杈撳嚭璇勪及缁撴灉锛屽寘鍚?hit_rate 鍜?MRR 鎸囨爣 |
| I-02 | 鎸囧畾鑷畾涔?golden test set | Baseline | 1. 鎵ц `python scripts/evaluate.py --test-set tests/fixtures/golden_test_set.json` | 浣跨敤椤圭洰鑷甫鐨?golden test set锛? 鏉℃祴璇曠敤渚嬶級杩愯璇勪及锛岃緭鍑哄悇椤规寚鏍?|
| I-03 | --json 鏍煎紡杈撳嚭 | Baseline | 1. 鎵ц `python scripts/evaluate.py --json` | 杈撳嚭 JSON 鏍煎紡缁撴灉锛堣€岄潪鏍煎紡鍖栨枃鏈級锛屽彲琚▼搴忚В鏋?|
| I-04 | --no-search 妯″紡 | Any | 1. 鎵ц `python scripts/evaluate.py --no-search` | 璺宠繃瀹為檯妫€绱紝杩涜 mock 璇勪及锛堥獙璇佽瘎浼版鏋舵湰韬彲鐢級 |
| I-05 | golden test set 涓嶅瓨鍦ㄦ椂鎶ラ敊 | Any | 1. 鎵ц `python scripts/evaluate.py --test-set /涓嶅瓨鍦?json` | 杈撳嚭鏂囦欢鏈壘鍒扮殑閿欒淇℃伅锛宔xit code 鈮?0 |

---

## J. MCP Server 鍗忚浜や簰

> 鍚姩鏂瑰紡: MCP Client (濡?VS Code Copilot/Claude Desktop) 閫氳繃 Stdio 鍚姩 `python main.py`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| J-01 | MCP Server 姝ｅ父鍚姩 | Baseline | 1. 鍦?VS Code 鐨?MCP 閰嶇疆涓坊鍔?Server锛屾寚鍚?`python main.py`<br>2. 閲嶅惎 VS Code / 閲嶆柊鍔犺浇 | MCP Server 鎴愬姛鍚姩锛孷S Code 鏄剧ず杩炴帴鎴愬姛 |
| J-02 | tools/list 杩斿洖宸ュ叿鍒楄〃 | Baseline | 1. 鍦?Copilot 涓Е鍙戝伐鍏峰垪琛紙鎴栫洿鎺ュ彂閫?JSON-RPC tools/list锛?| 杩斿洖 3 涓伐鍏凤細query_knowledge_hub銆乴ist_collections銆乬et_document_summary |
| J-03 | query_knowledge_hub 鏌ヨ | Baseline | 1. 鍦?Copilot 鑱婂ぉ涓彁闂?"What is hybrid search and how does it work?"锛堝搴?golden_test_set.json 涓殑娴嬭瘯鐢ㄤ緥锛?br>2. 璁?Copilot 璋冪敤 query_knowledge_hub 宸ュ叿 | 杩斿洖缁撴瀯鍖栫粨鏋滐紝鍖呭惈鏂囨湰鍐呭鍜屽紩鐢ㄤ俊鎭紙source_file=complex_technical_doc.pdf銆乸age銆乻core锛夛紝鏂囨湰涓簲鍚?"dense"銆?sparse"銆?BM25" 鎴?"RRF" 绛夋贩鍚堟绱㈢浉鍏冲叧閿瘝 |
| J-04 | list_collections 鍔熻兘 | Baseline | 1. 瑙﹀彂 list_collections 宸ュ叿璋冪敤 | 杩斿洖鎵€鏈夐泦鍚堝悕绉板拰鏂囨。鏁伴噺缁熻 |
| J-05 | get_document_summary 鍔熻兘 | Baseline | 1. 瑙﹀彂 get_document_summary 宸ュ叿璋冪敤锛屼紶鍏?doc_id 涓?simple.pdf 鐨勬枃妗?ID锛堝彲鍏堥€氳繃 list_collections 鑾峰彇锛?| 杩斿洖 simple.pdf 鐨?title锛堝簲鍚?"Sample Document"锛夈€乻ummary銆乼ags 鍏冧俊鎭紝鍐呭涓庢枃妗ｅ疄闄呭唴瀹瑰尮閰?|
| J-06 | 鏌ヨ杩斿洖鍚浘鐗囩殑澶氭ā鎬佺粨鏋?| Baseline | 1. 鍦?Copilot 涓皟鐢?query_knowledge_hub锛宷uery 鍙傛暟涓?"embedded image document with images"锛宑ollection 鍙傛暟涓?"default" | 杩斿洖鐨?content 鏁扮粍涓寘鍚?TextContent 鍜?ImageContent锛圔ase64锛夛紝寮曠敤淇℃伅涓?source_file 涓?with_images.pdf锛孋opilot 涓彲鐪嬪埌鍥剧墖鎴栧浘鐗囨弿杩帮紙caption 鏂囨湰锛?|
| J-07 | 鏌ヨ涓嶅瓨鍦ㄧ殑闆嗗悎 | Any | 1. 璋冪敤 query_knowledge_hub锛宑ollection 鍙傛暟鎸囧畾 "nonexistent_collection_xyz" | 杩斿洖绌虹粨鏋滄垨鍙嬪ソ閿欒鎻愮ず锛堝 "Collection not found"锛夛紝涓嶅鑷?Server 宕╂簝 |
| J-08 | 鏃犳晥鍙傛暟澶勭悊 | Baseline | 1. 鍙戦€佷竴涓己灏?query 鍙傛暟鐨?query_knowledge_hub 璋冪敤 | 杩斿洖 JSON-RPC 閿欒鐮侊紙濡?InvalidParams锛夛紝閿欒鎻忚堪娓呮櫚 |
| J-09 | Server 闀挎椂闂磋繍琛岀ǔ瀹氭€?| Baseline | 1. 淇濇寔 Server 杩愯 30 鍒嗛挓<br>2. 鏈熼棿鎵ц浠ヤ笅 5 娆℃煡璇紙姣忛殧 5 鍒嗛挓涓€娆★級锛?br>  a. "What is Modular RAG?"<br>  b. "How to configure Azure OpenAI?"<br>  c. "Explain the chunking strategy"<br>  d. "What is hybrid search?"<br>  e. "What evaluation metrics are supported?" | 鎵€鏈?5 娆℃煡璇㈠潎姝ｅ父鍝嶅簲锛堣繑鍥炴绱㈢粨鏋滐級锛屾棤鍐呭瓨娉勬紡杩硅薄锛屾棤瓒呮椂锛屽搷搴旀椂闂存棤鏄庢樉澧為暱 |
| J-10 | 寮曠敤閫忔槑鎬ф鏌?| Baseline | 1. 璋冪敤 query_knowledge_hub锛宷uery="Sample Document PDF loader"锛宑ollection="default"<br>2. 妫€鏌ヨ繑鍥炵粨鏋滅殑寮曠敤淇℃伅 | 姣忎釜妫€绱㈢墖娈靛寘鍚?source_file锛堝€间负 "simple.pdf"锛夈€乸age锛堝€间负 1锛夈€乧hunk_id锛堥潪绌哄瓧绗︿覆锛夈€乻core锛堝垎鏁板湪 0-1 涔嬮棿锛夛紝鏀寔婧簮 |

---

## K. Provider 鍒囨崲 鈥?DeepSeek LLM

> **鍓嶆彁**: 鑾峰彇鏈夋晥鐨?DeepSeek API Key  
> **鑼冨洿**: DeepSeek 浠呮湁 LLM锛堟枃鏈璇濓級锛屾棤 Embedding API锛屾棤 Vision API  
> **鍒囨崲鏂瑰紡**: 淇敼 `config/settings.yaml`

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| K-01 | settings.yaml 鍒囨崲 LLM 鍒?DeepSeek | DeepSeek | 1. 鎵ц `python .github/skills/qa-tester/scripts/qa_config.py apply deepseek`<br>2. 妫€鏌ヨ緭鍑虹‘璁ゅ垏鎹㈡垚鍔?| 杈撳嚭鏄剧ず "LLM -> deepseek / deepseek-chat"锛宻ettings.yaml 宸叉洿鏂?|
| K-02 | DeepSeek LLM 鈥?CLI 鏌ヨ | DeepSeek | 1. 鎵ц `python scripts/query.py --query "What is hybrid search and how does it work" --verbose` | 鏌ヨ鎴愬姛锛岃繑鍥炴绱㈢粨鏋滐紙鏉ヨ嚜 Baseline 鏁版嵁锛夈€俈erbose 杈撳嚭涓彲鐪嬪埌 LLM provider 涓?DeepSeek |
| K-03 | DeepSeek LLM 鈥?鎽勫彇锛圕hunk Refiner锛?| DeepSeek | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force --verbose` | Transform 闃舵浣跨敤 DeepSeek 杩涜 Chunk 閲嶅啓锛屾棩蹇楀彲瑙併€傞噸鍐欏悗鐨?Chunk 鍐呭鍚堢悊銆佷腑鏂囬€氶『 |
| K-04 | DeepSeek LLM 鈥?鎽勫彇锛圡etadata Enricher锛?| DeepSeek | 1. 鍚?K-03 鎽勫彇娴佺▼<br>2. 鏌ョ湅 Dashboard Data Browser 涓殑 Chunk Metadata | Metadata 涓?title/summary/tags 瀛楁鐢?DeepSeek 鐢熸垚锛屽唴瀹瑰悎鐞?|
| K-05 | DeepSeek LLM 鈥?Dashboard Overview 鍙嶆槧閰嶇疆 | DeepSeek | 1. 鎵撳紑 Dashboard Overview 椤甸潰 | LLM 鍗＄墖鏄剧ず provider=deepseek, model=deepseek-chat |
| K-06 | DeepSeek LLM 鈥?Dashboard Ingestion 绠＄悊 | DeepSeek | 1. 鍦?Dashboard Ingestion Manager 涓婁紶 `tests/fixtures/sample_documents/chinese_technical_doc.pdf` 骞舵憚鍙栧埌 default 闆嗗悎 | 杩涘害鏉℃甯告帹杩涳紝Transform 闃舵浣跨敤 DeepSeek LLM 瀹屾垚 Chunk Refine 鍜?Metadata Enrich锛屾渶缁堟垚鍔熴€侱ata Browser 涓彲鐪嬪埌璇ユ枃妗?|
| K-07 | DeepSeek LLM 鈥?鍏抽棴 Vision LLM | DeepSeek | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/with_images.pdf --force --verbose` | 鍥剧墖 Captioning 璺宠繃锛堝洜 DeepSeek 鏃?Vision API锛夛紝涓嶉樆濉炴祦绋嬨€傛棩蹇椾腑鏄剧ず璺宠繃 captioning锛寃ith_images.pdf 鐨?Chunk 涓浘鐗囧紩鐢ㄤ繚鐣欎絾鏃?caption 鏂囨湰 |
| K-08 | DeepSeek LLM 鈥?LLM Rerank 妯″紡 | DeepSeek | 1. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation modular architecture" --verbose` | Rerank 闃舵浣跨敤 DeepSeek LLM 杩涜閲嶆帓搴忥紝Verbose 杈撳嚭鍙閲嶆帓鍓嶅悗鐨勯『搴忓彉鍖栵紝缁撴灉鏉ヨ嚜 complex_technical_doc.pdf |
| K-09 | DeepSeek 鍥為€€ Azure 楠岃瘉 | DeepSeek | 1. 鎵ц `python .github/skills/qa-tester/scripts/qa_config.py restore`<br>2. 鎵ц `python scripts/query.py --query "Sample Document PDF loader" --verbose` | 鍔熻兘鎭㈠姝ｅ父锛孷erbose 杈撳嚭鏄剧ず浣跨敤 Azure LLM锛屾煡璇㈢粨鏋滃寘鍚?simple.pdf 鐩稿叧鍐呭锛岄獙璇佸垏鎹㈠洖鏉ユ棤鍓綔鐢?|
| K-10 | DeepSeek API Key 鏃犳晥鐨勬姤閿?| DeepSeek | 1. 璁剧疆 `llm.provider: deepseek`锛宍api_key` 濉叆涓€涓棤鏁堝€?br>2. 鎵ц鏌ヨ | 杩斿洖娓呮櫚鐨勮璇佸け璐ラ敊璇俊鎭紙濡?401 Unauthorized锛夛紝涓嶅穿婧?|
| K-11 | DeepSeek + Azure Embedding 娣峰悎閰嶇疆 | DeepSeek | 1. 淇濇寔 embedding 涓?azure<br>2. 鎵ц瀹屾暣鐨?ingest鈫抭uery 娴佺▼ | 鎽勫彇浣跨敤 Azure Embedding 鐢熸垚鍚戦噺 + DeepSeek LLM 鍋?Transform锛涙煡璇娇鐢?Azure Embedding 鍋氬悜閲忔绱?+ DeepSeek 鍋?Rerank锛堝鍚敤锛夈€傚叏娴佺▼璺戦€?|
| K-12 | Ragas 璇勪及浣跨敤 DeepSeek LLM | DeepSeek | 1. 鍦?Dashboard Evaluation Panel 閫夋嫨 ragas 鍚庣<br>2. 杩愯璇勪及 | Ragas 浣跨敤 DeepSeek 浣滀负 Judge LLM锛岃繑鍥炶瘎浼版寚鏍囥€傦紙娉ㄦ剰锛歊agas 鍙兘瀵?LLM 鑳藉姏鏈夎姹傦紝瑙傚療缁撴灉鏄惁鍚堢悊锛?|

---

## L. Provider 鍒囨崲 鈥?Reranker 妯″紡

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| L-01 | Reranker=None 妯″紡锛堥粯璁わ級 | Baseline | 1. 鎵ц `python scripts/query.py --query "What is hybrid search and how does it work" --verbose` | Verbose 杈撳嚭鏄剧ず Rerank 闃舵琚烦杩囷紝鏈€缁堢粨鏋?= RRF 铻嶅悎缁撴灉锛岀粨鏋滃寘鍚?complex_technical_doc.pdf 鐨?Chunk |
| L-02 | 鍒囨崲鍒?LLM Reranker | Rerank_LLM | 1. 鎵ц `python scripts/query.py --query "Explain the chunking strategy and how documents are split" --verbose` | Verbose 杈撳嚭鏄剧ず Rerank 浣跨敤 LLM 鎵撳垎锛岀粨鏋滃寘鍚?LLM 鐨勭浉鍏虫€ц瘎鍒嗭紝閲嶆帓鍚庢帓搴忓彲鑳戒笌 RRF 铻嶅悎缁撴灉涓嶅悓 |
| L-03 | Rerank 鍓嶅悗瀵规瘮锛圦uery Traces锛?| Rerank_LLM | 1. 鎵撳紑 Dashboard Query Traces<br>2. 灞曞紑鏈€鏂扮殑鏌ヨ Trace<br>3. 瀵规瘮 Fusion Tab 鍜?Rerank Tab | Rerank 涔嬪悗鐨勬帓搴忎笌 Fusion 鎺掑簭涓嶅悓锛堟煇浜?Chunk 鎺掑悕涓婂崌/涓嬮檷锛?|
| L-04 | Reranker top_k 鍙傛暟鐢熸晥 | Rerank_LLM | 1. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation modular architecture" --verbose` | Rerank 鍚庢渶缁堣繑鍥?3 鏉＄粨鏋滐紙鑰岄潪 Fusion 鐨?10 鏉★級锛岀粨鏋滃簲涓昏鏉ヨ嚜 complex_technical_doc.pdf |
| L-05 | Reranker 澶辫触鍚?Fallback | Rerank_LLM | 1. 灏?`llm.api_key` 涓存椂鏀逛负鏃犳晥鍊?br>2. 鎵ц `python scripts/query.py --query "performance benchmarks Precision Recall" --verbose` | 鎺у埗鍙版樉绀?Rerank 澶辫触鐨勮鍛婏紝浣嗘煡璇粛杩斿洖缁撴灉锛團allback 鍒?RRF 鎺掑簭锛夛紝涓嶅穿婧?|

---

## M. 閰嶇疆鍙樻洿涓庡閿?

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| M-01 | Azure LLM API key 閿欒 | InvalidKey | 1. 灏?`llm.api_key` 鏀逛负 "invalid_key_12345"<br>2. 鎵ц `python scripts/query.py --query "娴嬭瘯"` | 缁堢杈撳嚭娓呮櫚鐨?API 璁よ瘉閿欒锛堝 "401 Unauthorized" 鎴?"Invalid API key"锛夛紝exit code 鈮?0 |
| M-02 | Azure Embedding API key 閿欒 | InvalidEmbedKey | 1. 灏?`embedding.api_key` 鏀逛负鏃犳晥鍊?br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force` | 鍦?Embed 闃舵鎶ラ敊锛岄敊璇俊鎭槑纭寚鍚?Embedding API 闂锛堝 "401 Unauthorized" 鎴?"Invalid API key"锛?|
| M-03 | Azure Endpoint URL 閿欒 | Baseline | 1. 灏?`llm.azure_endpoint` 鏀逛负 "https://invalid.openai.azure.com/"<br>2. 鎵ц `python scripts/query.py --query "Sample Document PDF loader"` | 杈撳嚭杩炴帴澶辫触鎴?DNS 瑙ｆ瀽澶辫触鐨勯敊璇紝涓嶆寕璧蜂笉鍗℃锛宔xit code 鈮?0 |
| M-04 | Vision LLM 鍏抽棴鍚庣殑鎽勫彇 | NoVision | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/with_images.pdf --force --verbose` | 鎽勫彇鎴愬姛瀹屾垚锛屾棩蹇椾腑鏄剧ず鍥剧墖 Captioning 璺宠繃銆侱ashboard Ingestion Trace 鐨?Transform Tab 鏄剧ず captioned=0锛屼絾 Chunk 鏁伴噺姝ｅ父 |
| M-05 | settings.yaml 璇硶閿欒 | Baseline | 1. 鍦?settings.yaml 涓紩鍏?YAML 璇硶閿欒锛堝缂哄皯鍐掑彿锛?br>2. 鎵ц `python scripts/query.py --query "娴嬭瘯"` | 杈撳嚭閰嶇疆鏂囦欢瑙ｆ瀽閿欒鐨勬竻鏅版彁绀猴紝exit code=2 |
| M-06 | settings.yaml 缂哄皯蹇呭～瀛楁 | Baseline | 1. 鍒犻櫎 `embedding` 鏁翠釜閰嶇疆娈?br>2. 鎵ц鎽勫彇 | 杈撳嚭鏄庣‘鐨勭己灏戦厤缃」鐨勯敊璇彁绀?|
| M-07 | Chroma 鏁版嵁鐩綍涓嶅瓨鍦?| Baseline | 1. 灏?`vector_store.persist_directory` 鏀逛负涓€涓笉瀛樺湪鐨勮矾寰?br>2. 鎵ц鎽勫彇 | 鑷姩鍒涘缓鐩綍鎴栬緭鍑烘竻鏅伴敊璇?|
| M-08 | traces.jsonl 琚垹闄ゅ悗鐨?Dashboard | Baseline | 1. 鎵嬪姩鍒犻櫎 `logs/traces.jsonl`<br>2. 鍒锋柊 Dashboard 鍚勯〉闈?| Overview锛氭樉绀?"No traces recorded yet"锛汭ngestion/Query Traces锛氭樉绀虹┖鐘舵€佹彁绀恒€備笉宕╂簝涓嶆姤閿?|
| M-09 | traces.jsonl 鍚崯鍧忚 | Baseline | 1. 鍦?`logs/traces.jsonl` 涓墜鍔ㄦ彃鍏ヤ竴琛岄潪 JSON 鍐呭锛堝 "broken line"锛?br>2. 鍒锋柊 Dashboard Traces 椤甸潰 | 姝ｅ父璺宠繃鎹熷潖琛岋紝鍏朵粬 Trace 姝ｅ父灞曠ず |
| M-10 | Chunk Size 鍙傛暟璋冩暣 | Baseline | 1. 灏?`ingestion.chunk_size` 浠?1000 鏀逛负 500<br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force`<br>3. 鍦?Dashboard Data Browser 鏌ョ湅 simple.pdf 鐨?Chunk 鏁伴噺 | 鐢熸垚鏇村鏇寸煭鐨?Chunk锛堟暟閲忓簲姣?chunk_size=1000 鏃跺锛夛紝姣忎釜 Chunk 鏂囨湰闀垮害 鈮?500 瀛楃锛堢害锛?|
| M-11 | Chunk Overlap 鍙傛暟璋冩暣 | Baseline | 1. 灏?`ingestion.chunk_overlap` 浠?200 鏀逛负 0<br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force`<br>3. 鍦?Dashboard Data Browser 灞曞紑 simple.pdf 鐨勭浉閭?Chunk | Chunk 涔嬮棿鏃犻噸鍙犳枃鏈紙鐩搁偦 Chunk 鐨勫紑澶翠笉搴斾笌鍓嶄竴涓?Chunk 鐨勭粨灏鹃噸澶嶏級 |
| M-12 | 鍏抽棴 LLM Chunk Refiner | Baseline | 1. 灏?`ingestion.chunk_refiner.provider` 鏀逛负闈?LLM 妯″紡锛堝 rule-based锛?br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force --verbose`<br>3. 鍦?Dashboard Data Browser 鏌ョ湅 Chunk 鍐呭 | Transform 浣跨敤瑙勫垯鏂瑰紡锛堥潪 LLM锛夌簿绠€ Chunk锛屾憚鍙栭€熷害鏇村揩锛堟棩蹇楁棤 LLM 璋冪敤璁板綍锛夛紝Chunk 鏂囨湰涓庡師濮?Split 缁撴灉鏇存帴杩?|
| M-13 | 鍏抽棴 LLM Metadata Enricher | Baseline | 1. 灏?`ingestion.metadata_enricher.provider` 鏀逛负闈?LLM 妯″紡锛堝 rule-based锛?br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --force`<br>3. 鍦?Dashboard Data Browser 鏌ョ湅 simple.pdf 鐨?Chunk Metadata | Metadata 涓?title/summary/tags 鐢辫鍒欐柟寮忕敓鎴愶紙鍙兘涓虹┖鎴栫畝鐣ワ級锛屾棤 LLM 澧炲己鍐呭锛宻ummary 涓嶄細鏄?LLM 缂栧啓鐨勮嚜鐒惰瑷€鎽樿 |
| M-14 | 璋冩暣 retrieval.dense_top_k | Baseline | 1. 灏?`retrieval.dense_top_k` 浠?20 鏀逛负 5<br>2. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation" --verbose` | Dense 璺彫鍥炴渶澶?5 鏉＄粨鏋滐紙Verbose 涓?Dense Results 鏁伴噺 鈮?5锛夛紝鍑忓皯鍊欓€夐泦澶у皬 |
| M-15 | 璋冩暣 retrieval.rrf_k 甯告暟 | Baseline | 1. 灏?`retrieval.rrf_k` 浠?60 鏀逛负 10<br>2. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation" --verbose`<br>3. 瀵规瘮涓?rrf_k=60 鏃剁殑铻嶅悎鎺掑簭 | RRF 铻嶅悎浣跨敤涓嶅悓鐨勫钩婊戝父鏁帮紙k=10 浼氳鎺掑悕闈犲墠鐨勭粨鏋滄潈閲嶆洿澶э級锛孷erbose 涓彲瑙?fusion 鍒嗘暟鍙樺寲 |

---

## N. 鏁版嵁鐢熷懡鍛ㄦ湡闂幆

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| N-01 | 瀹屾暣闂幆: 鎽勫彇鈫掓煡璇⑩啋鍒犻櫎鈫掓煡璇?| Empty | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf`<br>2. 鎵ц `python scripts/query.py --query "Sample Document PDF loader"` 鈫?纭鍛戒腑<br>3. 鍦?Dashboard Data Browser 鍒犻櫎 default 闆嗗悎涓殑 simple.pdf<br>4. 鍐嶆鎵ц `python scripts/query.py --query "Sample Document PDF loader"` | 姝ラ 2 杩斿洖缁撴灉锛宻ource_file 鍚?simple.pdf锛涙楠?4 涓嶅啀杩斿洖 simple.pdf 鐩稿叧缁撴灉锛堢粨鏋滀负绌烘垨浠呭惈鍏朵粬鏂囨。锛?|
| N-02 | 鍒犻櫎鍚庨噸鏂版憚鍙?| Baseline | 1. 鍦?Dashboard 鍒犻櫎 default 闆嗗悎涓殑 simple.pdf<br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf`<br>3. 鎵ц `python scripts/query.py --query "Sample Document PDF loader"` | 鎽勫彇鎴愬姛锛團ileIntegrity 璁板綍宸叉竻鐞嗭紝涓嶄細琚烦杩囷級锛屾煡璇㈤噸鏂板懡涓?simple.pdf 鐨?Chunk |
| N-03 | 澶氶泦鍚堥殧绂婚獙璇?| Baseline | 1. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf --collection isolate_a`<br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/complex_technical_doc.pdf --collection isolate_b`<br>3. 鎵ц `python scripts/query.py --query "Sample Document PDF loader" --collection isolate_a`<br>4. 鎵ц `python scripts/query.py --query "Retrieval-Augmented Generation" --collection isolate_b` | 闆嗗悎 isolate_a 鏌ヨ浠呰繑鍥?simple.pdf 鍐呭锛坰ource_file=simple.pdf锛夛紱闆嗗悎 isolate_b 鏌ヨ浠呰繑鍥?complex_technical_doc.pdf 鍐呭锛屼簰涓嶅共鎵?|
| N-04 | Clear All Data 鍚庡叏鍔熻兘楠岃瘉 | Baseline | 1. Dashboard Clear All Data<br>2. 鎵ц `python scripts/query.py --query "Sample Document"` 鈫?鏃犵粨鏋?br>3. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/simple.pdf`<br>4. 鎵ц `python scripts/query.py --query "Sample Document PDF loader"` 鈫?鍛戒腑 | 娓呯┖鍚庢煡璇㈣繑鍥炵┖锛涢噸鏂版憚鍙?simple.pdf 鍚庢煡璇㈠懡涓紝绯荤粺瀹屽叏鎭㈠姝ｅ父 |
| N-05 | 鍚屼竴鏂囦欢鎽勫彇鍒板涓泦鍚?| Baseline | 1. 鎽勫彇 simple.pdf 鍒?collection_1<br>2. 鍐嶆鎽勫彇 simple.pdf 鍒?collection_2 | 涓や釜闆嗗悎鍚勮嚜鐙珛鎷ユ湁璇ユ枃妗ｇ殑 Chunk锛屼簰涓嶅奖鍝?|
| N-06 | 鍒犻櫎闆嗗悎 A 涓殑鏂囨。涓嶅奖鍝嶉泦鍚?B | Baseline | 1. 鍦?Dashboard 鍒犻櫎 collection_1 涓殑 simple.pdf<br>2. 鏌ヨ `--collection collection_2` | collection_2 涓殑鏁版嵁涓嶅彈褰卞搷锛屼粛鍙煡璇㈠懡涓?|

---

## O. 鏂囨。鏇挎崲涓庡鍦烘櫙楠岃瘉

> **閲嶇偣**: 浣跨敤涓嶅悓绫诲瀷鐨勪腑鏂?PDF 鏂囨。娴嬭瘯绯荤粺鐨勯€氱敤鎬? 
> **娴嬭瘯鏂囨。**: 椤圭洰鑷甫锛屼綅浜?`tests/fixtures/sample_documents/`锛堜腑鏂囨枃妗ｇ敱 `generate_qa_test_pdfs.py` 鐢熸垚锛?

| ID | 娴嬭瘯鏍囬 | 鐘舵€?| 鎿嶄綔姝ラ | 棰勬湡鐜拌薄 |
|----|---------|------|---------|--------- |
| O-01 | 绾枃鏈腑鏂囨妧鏈枃妗?| Baseline | 1. 鎽勫彇 `chinese_technical_doc.pdf`<br>2. 鐢ㄤ腑鏂囧叧閿瘝鏌ヨ锛堝"Transformer 娉ㄦ剰鍔?銆?娣峰悎妫€绱?RRF"锛?| 姝ｇ‘鍒嗗潡锛屼腑鏂?jieba 鍒嗚瘝鐢熸晥锛圫parse 璺彲鍙洖锛夛紝鏌ヨ鍛戒腑鐩稿叧鍐呭 |
| O-02 | 鍚腑鏂囪〃鏍肩殑 PDF | Baseline | 1. 鎽勫彇 `chinese_table_chart_doc.pdf`<br>2. 鐢ㄨ〃鏍间腑鐨勬暟鎹叧閿瘝鏌ヨ锛堝"BGE-large-zh"銆?Cross-Encoder"锛?| 琛ㄦ牸鍐呭琚纭В鏋愬埌 Chunk 涓紝鏌ヨ鍙懡涓〃鏍兼暟鎹?|
| O-03 | 鍚浘琛?娴佺▼鍥剧殑 PDF | Baseline | 1. 纭繚 Vision LLM 鍚敤<br>2. 鎽勫彇 `chinese_table_chart_doc.pdf`<br>3. 鐢ㄥ浘琛ㄦ弿杩扮殑鍐呭鏌ヨ锛堝"娴佺▼鍥?銆?鑰楁椂鍒嗗竷"锛?| 鍥剧墖琚彁鍙栥€丆aption 琚敓鎴愶紝鏌ヨ鐩稿叧鍏抽敭淇℃伅鍙懡涓?|
| O-04 | 澶氶〉闀挎枃妗?(30+ 椤? | Baseline | 1. 鎽勫彇 `chinese_long_doc.pdf`<br>2. 鍒嗗埆鐢ㄦ枃妗ｅ墠鍗婇儴鍒嗭紙濡?Transformer 浣嶇疆缂栫爜"锛夊拰鍚庡崐閮ㄥ垎锛堝"椤圭洰瀹炴垬缁忛獙"锛夌殑鍐呭鏌ヨ | 鎵€鏈夐〉闈㈠潎琚鐞嗭紱鍓嶅悗閮ㄥ垎鍐呭鍧囧彲琚彫鍥烇紱Chunk 鐨?page metadata 姝ｇ‘ |
| O-05 | 鍖呭惈浠ｇ爜鍧楃殑鎶€鏈枃妗?| Baseline | 1. 鎽勫彇 `complex_technical_doc.pdf`锛堝惈澶ч噺鎶€鏈湳璇拰缁勪欢鍚嶏級<br>2. 鎵ц `python scripts/query.py --query "ChromaDB text-embedding-ada-002 vector storage"` | 浠ｇ爜鍧楀拰鎶€鏈湳璇淇濈暀鍦?Chunk 涓紙涓嶈鍒嗗潡鐮村潖锛夛紝閫氳繃鎶€鏈叧閿瘝 "ChromaDB" 鎴?"ada-002" 鍙彫鍥炲搴斿唴瀹规 |
| O-06 | 宸叉憚鍙?DEV_SPEC 鑷韩 | Baseline | 1. 鎽勫彇 DEV_SPEC.md锛堝鏋滄敮鎸?md 鏍煎紡锛?br>2. 鐢?golden test set 涓殑鏌ヨ娴嬭瘯 | 鏌ヨ "What is Modular RAG" 绛夊懡涓?DEV_SPEC 鐩稿叧鍐呭 |
| O-07 | 鏇挎崲鏂囨。鍚庨噸鏂拌瘎浼?| Baseline | 1. Dashboard Clear All Data<br>2. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/complex_technical_doc.pdf` 鈫?杩愯 `python scripts/evaluate.py` 鈫?璁板綍鍒嗘暟<br>3. Dashboard Clear All Data<br>4. 鎵ц `python scripts/ingest.py --path tests/fixtures/sample_documents/chinese_technical_doc.pdf` 鈫?杩愯 `python scripts/evaluate.py` 鈫?璁板綍鍒嗘暟 | complex_technical_doc.pdf 鐨勮瘎浼板垎鏁板簲杈冮珮锛堣嫳鏂囧唴瀹逛笌 golden_test_set 鍖归厤搴﹂珮锛夛紱chinese_technical_doc.pdf 鐨勫垎鏁板簲杈冧綆锛堜腑鏂囧唴瀹逛笌鑻辨枃 golden_test_set 鍖归厤搴︿綆锛?|
| O-08 | 鎵弿鐩綍鎵归噺鎽勫彇澶氫唤 PDF | Baseline | 1. `python scripts/ingest.py --path tests/fixtures/sample_documents/` | 鎵€鏈?PDF 渚濇琚鐞嗭紝缁堢杈撳嚭澶勭悊姹囨€伙紙鎴愬姛鏁?鎬绘暟锛夛紝Dashboard 鍙湅鍒版墍鏈夋枃妗?|
| O-09 | 鍗氬/闈炴妧鏈被鐭枃妗?| Baseline | 1. 鎽勫彇 `blogger_intro.pdf`锛堝崥涓昏嚜鎴戜粙缁嶇被鐭枃妗ｏ級<br>2. 鐢ㄦ枃妗ｅ唴瀹瑰叧閿瘝鏌ヨ锛堝"鍗氬"銆?鑷垜浠嬬粛"锛?| 鐭枃妗ｆ纭垎鍧楋紙Chunk 鏁伴噺杈冨皯锛夛紝鏌ヨ鍙懡涓浉鍏冲唴瀹癸紝楠岃瘉闈炴妧鏈被鏂囨。鐨勬憚鍙栧吋瀹规€?|

---

## 闄勫綍锛氭祴璇曠幆澧冨噯澶囨竻鍗?

### 閰嶇疆鏂囦欢澶囦唤

| 鏂囦欢 | 鐢ㄩ€?| 璇存槑 |
|------|------|------|
| `config/settings.yaml` | 鍩虹嚎 Azure 閰嶇疆 | 娴嬭瘯鍓嶅浠戒负 `settings.yaml.bak` |
| `config/settings_deepseek.yaml` | DeepSeek LLM 閰嶇疆 | 澶嶅埗 settings.yaml锛屼慨鏀?llm 涓?deepseek |
| `config/settings_rerank_llm.yaml` | LLM 閲嶆帓閰嶇疆 | 淇敼 rerank 涓?llm |

### 娴嬭瘯鏂囨。

鎵€鏈夋祴璇曟枃妗ｅ潎宸插寘鍚湪椤圭洰涓紝浣嶄簬 `tests/fixtures/sample_documents/`锛屾棤闇€棰濆鍑嗗銆?

| 鏂囨。 | 璇存槑 |
|------|------|
| `simple.pdf` | 绠€鍗曠函鏂囨湰 PDF |
| `with_images.pdf` | 鍚祵鍏ュ浘鐗囩殑 PDF |
| `complex_technical_doc.pdf` | 澶氶〉鑻辨枃鎶€鏈枃妗ｏ紝鍚〃鏍煎拰鍥剧墖 |
| `chinese_technical_doc.pdf` | 绾腑鏂囨妧鏈枃妗ｏ紙~9 椤碉級锛屾兜鐩?LLM/RAG/Agent 绛夊唴瀹?|
| `chinese_table_chart_doc.pdf` | 鍚腑鏂囪〃鏍煎拰娴佺▼鍥剧殑 PDF锛垀6 椤碉級 |
| `chinese_long_doc.pdf` | 30+ 椤典腑鏂囬暱鏂囨。锛?5 绔犲ぇ妯″瀷闈㈣瘯鐭ヨ瘑鎵嬪唽 |
| `blogger_intro.pdf` | 鍗氫富鑷垜浠嬬粛绫荤煭鏂囨。锛岄潪鎶€鏈唴瀹?|
| `sample.txt` | 绾枃鏈枃浠讹紝楠岃瘉闈?PDF 鏍煎紡鏀寔 |

### API Key 鍑嗗

| Provider | 鐢ㄩ€?| 鎵€闇€ Key | 閰嶇疆鏂规硶 |
|----------|------|----------|---------|
| Azure OpenAI | 鍩虹嚎 LLM + Embedding + Vision | `api_key` (宸叉湁) | 宸插湪 settings.yaml 涓厤缃?|
| DeepSeek | 鏇夸唬 LLM 娴嬭瘯 (K 绯诲垪) | `DEEPSEEK_API_KEY` | 瑙佷笅鏂硅鏄?|

#### 澶栭儴 API Key 閰嶇疆姝ラ

K 绯诲垪娴嬭瘯闇€瑕?DeepSeek API Key銆?*涓€娆￠厤缃紝鎵€鏈夋祴璇曡嚜鍔ㄤ娇鐢?*銆?

```powershell
# 姝ラ 1: 澶嶅埗妯℃澘鏂囦欢
Copy-Item config/test_credentials.yaml.example config/test_credentials.yaml

# 姝ラ 2: 缂栬緫鏂囦欢锛屽～鍏ヤ綘鐨?API Key
# 鎵撳紑 config/test_credentials.yaml锛屽皢 <YOUR_DEEPSEEK_API_KEY> 鏇挎崲涓虹湡瀹?Key

# 姝ラ 3: 楠岃瘉閰嶇疆
python .github/skills/qa-tester/scripts/qa_config.py check
```

璇ユ枃浠跺凡娣诲姞鍒?`.gitignore`锛屼笉浼氳鎻愪氦鍒?Git锛屽彲瀹夊叏瀛樺偍 API Key銆?

#### 閰嶇疆鍒囨崲鏂瑰紡

娴嬭瘯鑴氭湰閫氳繃棰勫畾涔夌殑"閰嶇疆 Profile"鑷姩鍒囨崲 settings.yaml锛屾棤闇€鎵嬪姩缂栬緫锛?

```powershell
# 鏌ョ湅鍙敤 Profile
python .github/skills/qa-tester/scripts/qa_config.py show

# 鍒囨崲鍒?DeepSeek锛堣嚜鍔ㄥ浠?settings.yaml锛屾敞鍏?API Key锛?
python .github/skills/qa-tester/scripts/qa_config.py apply deepseek

# 鎵ц娴嬭瘯...

# 娴嬭瘯瀹屾垚鍚庢仮澶嶅師濮嬮厤缃?
python .github/skills/qa-tester/scripts/qa_config.py restore
```

| Profile 鍚嶇О | 鐢ㄩ€?| 瀵瑰簲娴嬭瘯 | 闇€瑕?Credentials |
|-------------|------|---------|-----------------|
| `deepseek` | LLM 鍒囨崲鍒?DeepSeek + 鍏抽棴 Vision | K-01~K-12 | 鏄?|
| `rerank_llm` | 鍚敤 LLM 閲嶆帓 | L-02 | 鍚?|
| `no_vision` | 鍏抽棴 Vision LLM | M-04 | 鍚?|
| `invalid_llm_key` | 璁剧疆鏃犳晥 LLM Key | M-01 | 鍚?|
| `invalid_embed_key` | 璁剧疆鏃犳晥 Embedding Key | M-02 | 鍚?|

---

> **缁熻**: 鍏?**117** 鏉℃祴璇曠敤渚?

