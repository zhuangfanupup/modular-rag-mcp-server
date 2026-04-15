## 3. 鎶€鏈€夊瀷

### 3.1 RAG 鏍稿績娴佹按绾胯璁?

#### 3.1.1 鏁版嵁鎽勫彇娴佹按绾?

**鐩爣锛?* 鏋勫缓缁熶竴銆佸彲閰嶇疆涓斿彲瑙傛祴鐨勬暟鎹憚鍙栨祦姘寸嚎锛岃鐩栨枃妗ｅ姞杞姐€佹牸寮忚В鏋愩€佽涔夊垏鍒嗐€佸妯℃€佸寮恒€佸祵鍏ヨ绠椼€佸幓閲嶄笌鎵归噺涓婅浇鍒板悜閲忓瓨鍌ㄣ€傝鑳藉姏搴旀槸鍙噸鐢ㄧ殑搴撴ā鍧楋紝渚夸簬鍦?`ingest.py`銆丏ashboard 绠＄悊闈㈡澘銆佺绾挎壒澶勭悊鍜屾祴璇曚腑璋冪敤銆?

- **鑷爺 Pipeline 妗嗘灦锛堣璁＄伒鎰熷弬鑰?LlamaIndex 鍒嗗眰鎬濇兂锛屼絾涓嶄緷璧?LlamaIndex 搴擄級锛?*
	- 閲囩敤鑷畾涔夋娊璞℃帴鍙ｏ紙`BaseLoader`/`BaseSplitter`/`BaseTransform`/`BaseEmbedding`/`BaseVectorStore`锛夛紝瀹炵幇瀹屽叏鍙帶鐨勫彲鎻掓嫈鏋舵瀯銆?
	- 鏀寔鍙粍鍚堢殑 Loader -> Splitter -> Transform -> Embed -> Upsert 娴佺▼锛屼究浜庡疄鐜板彲瑙傛祴鐨勬祦姘寸嚎銆?
	- 涓庝富娴?embedding provider 鏈夎壇濂介€傞厤锛屾灦鏋勪腑缁熶竴浣跨敤 Chroma 浣滀负鍚戦噺瀛樺偍銆?


璁捐瑕佺偣锛?
- **鏄庣‘鍒嗗眰鑱岃矗**锛?
  - Loader锛氳礋璐ｆ妸鍘熷鏂囦欢瑙ｆ瀽涓虹粺涓€鐨?`Document` 瀵硅薄锛坄text` + `metadata`锛涚被鍨嬪畾涔夐泦涓湪 `src/core/types.py`锛夈€?*鍦ㄥ綋鍓嶉樁娈碉紝浠呭疄鐜?PDF 鏍煎紡鐨?Loader銆?*
		- 缁熶竴杈撳嚭鏍煎紡閲囩敤瑙勮寖鍖?Markdown浣滀负 `Document.text`锛氳繖鏍峰彲浠ユ洿濂界殑閰嶅悎鍚庨潰鐨凷plitte锛圠angchain RecursiveCharacterTextSplitte锛夛級鏂规硶浜у嚭楂樿川閲忓垏鍧椼€?
		- Loader 鍚屾椂鎶藉彇/琛ラ綈鍩虹 metadata锛堝 `source_path`, `doc_type=pdf`, `page`, `title/heading_outline`, `images` 寮曠敤鍒楄〃绛夛級锛屼负瀹氫綅銆佸洖婧笌鍚庣画 Transform 鎻愪緵渚濇嵁銆?
	- Splitter锛氬熀浜?Markdown 缁撴瀯锛堟爣棰?娈佃惤/浠ｇ爜鍧楃瓑锛変笌鍙傛暟閰嶇疆鎶?`Document` 鍒囦负鑻ュ共 Chunk锛屼繚鐣欏師濮嬩綅缃笌涓婁笅鏂囧紩鐢ㄣ€?
	- Transform锛氬彲鎻掑叆鐨勫鐞嗘楠わ紙ImageCaptioning銆丱CR銆乧ode-block normalization銆乭tml-to-text cleanup 绛夛級锛孴ransform 鍙互閫夋嫨鎶婇澶栦俊鎭拷鍔犲埌 chunk.text 鎴栨斁鍏?chunk.metadata锛堟帹鑽愰粯璁よ拷鍔犲埌 text 浠ヤ繚璇佹绱㈣鐩栵級銆?
	- Embed & Upsert锛氭寜鎵规璁＄畻 embedding锛屽苟涓婅浇鍒板悜閲忓瓨鍌紱鏀寔鍚戦噺 + metadata 涓婅浇锛屽苟鎻愪緵骞傜瓑 upsert 绛栫暐锛堝熀浜?id/hash锛夈€?
	- Dedup & Normalize锛氬湪涓婅浇鍓嶈繍琛屽悜閲?鏂囨湰鍘婚噸涓庡搱甯岃繃婊わ紝閬垮厤閲嶅绱㈠紩銆?

鍏抽敭瀹炵幇瑕佺礌锛?

- Loader锛堢粺涓€鏍煎紡涓庡厓鏁版嵁锛?
	- **鍓嶇疆鍘婚噸 (Early Exit / File Integrity Check)**锛?
		- 鏈哄埗锛氬湪瑙ｆ瀽鏂囦欢鍓嶏紝璁＄畻鍘熷鏂囦欢鐨?SHA256 鍝堝笇鎸囩汗銆?
		- 鍔ㄤ綔锛氭绱?`ingestion_history` 琛紝鑻ュ彂鐜扮浉鍚?Hash 涓旂姸鎬佷负 `success` 鐨勮褰曪紝鍒欒瀹氳鏂囦欢鏈彂鐢熷彉鏇达紝鐩存帴璺宠繃鍚庣画鎵€鏈夊鐞嗭紙瑙ｆ瀽銆佸垏鍒嗐€丩LM閲嶅啓锛夛紝瀹炵幇**闆舵垚鏈?(Zero-Cost)** 鐨勫閲忔洿鏂般€?
		- **瀛樺偍鏂规**锛堝垵鏈熷疄鐜帮紝鍙彃鎷旓級锛?
			- **榛樿閫夋嫨锛歋QLite**锛屽瓨鍌ㄤ簬 `data/db/ingestion_history.db`
			- **琛ㄧ粨鏋?*锛?
				```sql
				CREATE TABLE ingestion_history (
				    file_hash TEXT PRIMARY KEY,
				    file_path TEXT NOT NULL,
				    file_size INTEGER,
				    status TEXT NOT NULL CHECK(status IN ('success', 'failed', 'processing')),
				    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				    error_msg TEXT,
				    chunk_count INTEGER
				);
				CREATE INDEX idx_status ON ingestion_history(status);
				CREATE INDEX idx_processed_at ON ingestion_history(processed_at);
				```
			- **鏌ヨ閫昏緫**锛歚SELECT status FROM ingestion_history WHERE file_hash = ? AND status = 'success'`
			- **鏇挎崲璺緞**锛氬悗缁彲鍗囩骇涓?Redis锛堝垎甯冨紡缂撳瓨锛夋垨 PostgreSQL锛堜紒涓氱骇涓績鍖栧瓨鍌級
	
	> **馃搶 鎸佷箙鍖栧瓨鍌ㄦ灦鏋勭粺涓€璇存槑**
	> 
	> 鏈」鐩湪澶氫釜鏍稿績妯″潡涓噰鐢?**SQLite** 浣滀负杞婚噺绾ф寔涔呭寲瀛樺偍鏂规锛岄伩鍏嶅紩鍏ラ噸閲忕骇鏁版嵁搴撲緷璧栵紝淇濇寔鏈湴浼樺厛锛圠ocal-First锛夌殑璁捐鐞嗗康锛?
	> 
	> | 瀛樺偍妯″潡 | 鏁版嵁搴撴枃浠?| 鐢ㄩ€?| 琛ㄧ粨鏋勫叧閿瓧娈?|
	> |---------|-----------|------|---------------|
	> | **鏂囦欢瀹屾暣鎬ф鏌?* | `data/db/ingestion_history.db` | 璁板綍宸插鐞嗘枃浠剁殑 SHA256 鍝堝笇锛屽疄鐜板閲忔憚鍙?| `file_hash`, `status`, `processed_at` |
	> | **鍥剧墖绱㈠紩鏄犲皠** | `data/db/image_index.db` | 璁板綍 image_id 鈫?鏂囦欢璺緞鏄犲皠锛屾敮鎸佸浘鐗囨绱笌寮曠敤 | `image_id`, `file_path`, `collection` |
	> | **BM25 绱㈠紩鍏冩暟鎹?* | `data/db/bm25/` | 瀛樺偍鍊掓帓绱㈠紩鍜?IDF 缁熻淇℃伅锛堟湭鏉ュ彲鎵╁睍鐢?SQLite锛?| 褰撳墠浣跨敤 pickle锛屽彲杩佺Щ鑷?SQLite |
	> 
	> **璁捐浼樺娍**锛?
	> - **闆朵緷璧栭儴缃?*锛氭棤闇€瀹夎 MySQL/PostgreSQL 绛夋暟鎹簱鏈嶅姟锛宍pip install` 鍗冲彲杩愯
	> - **骞跺彂瀹夊叏**锛歐AL (Write-Ahead Logging) 妯″紡鏀寔澶氳繘绋嬪畨鍏ㄨ鍐?
	> - **鎸佷箙鍖栦繚璇?*锛氭憚鍙栧巻鍙插拰绱㈠紩鏄犲皠鍦ㄨ繘绋嬮噸鍚悗鑷姩鎭㈠锛岄伩鍏嶉噸澶嶈绠?
	> - **鏋舵瀯涓€鑷存€?*锛氭墍鏈?SQLite 妯″潡閬靛惊鐩稿悓鐨勫垵濮嬪寲銆佹煡璇笌閿欒澶勭悊妯″紡锛屼究浜庣淮鎶や笌鎵╁睍
	> 
	> **鍗囩骇璺緞**锛氬綋绯荤粺瑙勬ā鎵╁睍鑷冲垎甯冨紡鍦烘櫙鏃讹紝鍙€氳繃缁熶竴鐨勬娊璞℃帴鍙ｅ皢 SQLite 鏇挎崲涓?PostgreSQL 鎴?Redis锛屾棤闇€淇敼涓婂眰涓氬姟閫昏緫銆?
	
	- **瑙ｆ瀽涓庢爣鍑嗗寲**锛?
		- 褰撳墠鑼冨洿锛?*浠呭疄鐜?PDF -> canonical Markdown 瀛愰泦** 鐨勮浆鎹€?
	- 鎶€鏈€夊瀷锛圥ython PDF -> Markdown锛夛細
		- **棣栭€夛細MarkItDown**锛堜綔涓洪粯璁?PDF 瑙ｆ瀽/杞崲寮曟搸锛夈€備紭鐐规槸鐩存帴浜у嚭 Markdown 褰㈡€佹枃鏈紝渚夸簬涓庡悗缁?`RecursiveCharacterTextSplitter` 鐨?separators 閰嶅悎銆?
	- 杈撳嚭鏍囧噯 `Document`锛歚id|source|text(markdown)|metadata`銆俶etadata 鑷冲皯鍖呭惈 `source_path`, `doc_type`, `title/heading_outline`, `page/slide`锛堝閫傜敤锛? `images`锛堝浘鐗囧紩鐢ㄥ垪琛級銆?
	- Loader 涓嶈礋璐ｅ垏鍒嗭細鍙仛鈥滄牸寮忕粺涓€ + 缁撴瀯鎶藉彇 + 寮曠敤鏀堕泦鈥濓紝纭繚鍒囧垎绛栫暐鍙嫭绔嬭凯浠ｄ笌搴﹂噺銆?

- Splitter锛圠angChain 璐熻矗鍒囧垎锛涚嫭绔嬨€佸彲鎺э級
	- **瀹炵幇鏂规锛氫娇鐢?LangChain 鐨?`RecursiveCharacterTextSplitter` 杩涜鍒囧垎銆?*
		- 浼樺娍锛氳鏂规硶瀵?Markdown 鏂囨。鐨勭粨鏋勶紙鏍囬銆佹钀姐€佸垪琛ㄣ€佷唬鐮佸潡锛夋湁澶╃劧鐨勯€傞厤鎬э紝鑳藉閫氳繃閰嶇疆璇箟鏂偣锛圫eparators锛夊疄鐜伴珮璐ㄩ噺銆佽涔夊畬鏁寸殑鍒囧潡銆?
	- Splitter 杈撳叆锛歀oader 浜у嚭鐨?Markdown `Document`銆?
	- Splitter 杈撳嚭锛氳嫢骞?`Chunk`锛堟垨 Document-like chunks锛夛紝姣忎釜 chunk 蹇呴』鎼哄甫绋冲畾鐨勫畾浣嶄俊鎭笌鏉ユ簮淇℃伅锛歚source`, `chunk_index`, `start_offset/end_offset`锛堟垨绛変环瀹氫綅瀛楁锛夈€?

- Transform & Enrichment锛堢粨鏋勮浆鎹笌娣卞害澧炲己锛?
	鏈樁娈垫槸 ETL 绠￠亾鐨勬牳蹇冣€滄櫤鍔涒€濈幆鑺傦紝璐熻矗灏?Splitter 浜у嚭鐨勯潪缁撴瀯鍖栨枃鏈潡杞寲涓虹粨鏋勫寲銆佸瘜璇箟鐨勬櫤鑳藉垏鐗囷紙Smart Chunk锛夈€?
	- **缁撴瀯杞崲 (Structure Transformation)**锛氬皢鍘熷鐨?`String` 绫诲瀷鏁版嵁杞寲涓哄己绫诲瀷鐨?`Record/Object`锛屼负涓嬫父妫€绱㈡彁渚涘瓧娈电骇鏀寔銆?
	- **鏍稿績澧炲己绛栫暐**锛?
		1. **鏅鸿兘閲嶇粍 (Smart Chunking & Refinement)**锛?
			- 绛栫暐锛氬埄鐢?LLM 鐨勮涔夌悊瑙ｈ兘鍔涳紝瀵逛笂涓€闃舵鈥滅矖鍒囧垎鈥濈殑鐗囨杩涜浜屾鍔犲伐銆?
			- 鍔ㄤ綔锛氬悎骞跺湪閫昏緫涓婄揣瀵嗙浉鍏充絾琚墿鐞嗗垏鏂殑娈佃惤锛屽墧闄ゆ棤鎰忎箟鐨勯〉鐪夐〉鑴氭垨涔辩爜锛堝幓鍣級锛岀‘淇濇瘡涓?Chunk 鏄嚜鍖呭惈锛圫elf-contained锛夌殑璇箟鍗曞厓銆?
		2. **璇箟鍏冩暟鎹敞鍏?(Semantic Metadata Enrichment)**锛?
			- 绛栫暐锛氬湪鍩虹鍏冩暟鎹紙璺緞銆侀〉鐮侊級涔嬩笂锛屽埄鐢?LLM 鎻愬彇楂樼淮璇箟鐗瑰緛銆?
			- 浜у嚭锛氫负姣忎釜 Chunk 鑷姩鐢熸垚 `Title`锛堢簿鍑嗗皬鏍囬锛夈€乣Summary`锛堝唴瀹规憳瑕侊級鍜?`Tags`锛堜富棰樻爣绛撅級锛屽苟灏嗗叾娉ㄥ叆鍒?Metadata 瀛楁涓紝鏀寔鍚庣画鐨勬贩鍚堟绱笌绮剧‘杩囨护銆?
		3. **澶氭ā鎬佸寮?(Multimodal Enrichment / Image Captioning)**锛?
			- 绛栫暐锛氭壂鎻忔枃妗ｇ墖娈典腑鐨勫浘鍍忓紩鐢紝璋冪敤 Vision LLM锛堝 GPT-4o锛夎繘琛岃瑙夌悊瑙ｃ€?
			- 鍔ㄤ綔锛氱敓鎴愰珮淇濈湡鐨勬枃鏈弿杩帮紙Caption锛夛紝鎻忚堪鍥捐〃閫昏緫鎴栨彁鍙栨埅鍥炬枃瀛椼€?
			- 瀛樺偍锛氬皢 Caption 鏂囨湰鈥滅紳鍚堚€濊繘 Chunk 鐨勬鏂囨垨 Metadata 涓紝鎵撻€氭ā鎬侀殧闃傦紝瀹炵幇鈥滄悳鏂囧嚭鍥锯€濄€?
	- **宸ョ▼鐗规€?*锛歍ransform 姝ラ璁捐涓哄師瀛愬寲涓庡箓绛夋搷浣滐紝鏀寔閽堝鐗瑰畾 Chunk 鐨勭嫭绔嬮噸璇曚笌澧為噺鏇存柊锛岄伩鍏嶅洜 LLM 璋冪敤澶辫触瀵艰嚧鏁翠釜鏂囨。澶勭悊涓柇銆?

- **Embedding (鍙岃矾鍚戦噺鍖?**
	- **宸噺璁＄畻 (Incremental Embedding / Cost Optimization)**锛?
		- 绛栫暐锛氬湪璋冪敤鏄傝吹鐨?Embedding API 涔嬪墠锛岃绠?Chunk 鐨勫唴瀹瑰搱甯岋紙Content Hash锛夈€備粎閽堝鏁版嵁搴撲腑涓嶅瓨鍦ㄧ殑鏂板唴瀹瑰搱甯屾墽琛屽悜閲忓寲璁＄畻锛屽浜庢枃浠跺悕鍙樻洿浣嗗唴瀹规湭鍙樼殑鐗囨锛岀洿鎺ュ鐢ㄥ凡鏈夊悜閲忥紝鏄捐憲闄嶄綆 API 璋冪敤鎴愭湰銆?
	- **鏍稿績绛栫暐**锛氫负浜嗘敮鎸侀珮绮惧害鐨勬贩鍚堟绱紙Hybrid Search锛夛紝绯荤粺瀵规瘡涓?Chunk 骞惰鎵ц鍙岃矾缂栫爜璁＄畻銆?
		- **Dense Embeddings锛堣涔夊悜閲忥級**锛氳皟鐢?Embedding 妯″瀷锛堝 OpenAI text-embedding-3 鎴?BGE锛夌敓鎴愰珮缁存诞鐐瑰悜閲忥紝鎹曟崏鏂囨湰鐨勬繁灞傝涔夊叧鑱旓紝瑙ｅ喅鈥滆瘝涓嶅悓鎰忓悓鈥濈殑妫€绱㈤毦棰樸€?
		- **Sparse Embeddings锛堢█鐤忓悜閲忥級**锛氬埄鐢?BM25 缂栫爜鍣ㄦ垨 SPLADE 妯″瀷鐢熸垚绋€鐤忓悜閲忥紙Keyword Weights锛夛紝鎹曟崏绮剧‘鐨勫叧閿瘝鍖归厤淇℃伅锛岃В鍐充笓鏈夊悕璇嶆煡鎵鹃棶棰樸€?
	- **鎵瑰鐞嗕紭鍖?*锛氭墍鏈夎绠楀潎閲囩敤 `batch_size` 椹卞姩鐨勬壒澶勭悊妯″紡锛屾渶澶у寲 CPU 鍒╃敤鐜囧苟鍑忓皯缃戠粶 RTT銆?

- **Upsert & Storage (绱㈠紩瀛樺偍)**
	- **瀛樺偍鍚庣**锛氱粺涓€浣跨敤鍚戦噺鏁版嵁搴擄紙濡?Chroma/Qdrant锛変綔涓哄瓨鍌ㄥ紩鎿庯紝鍚屾椂鎸佷箙鍖栧瓨鍌?Dense Vector銆丼parse Vector 浠ュ強 Transform 闃舵鐢熸垚鐨勫瘜 Metadata銆?
	- **All-in-One 瀛樺偍绛栫暐**锛氭墽琛屽師瀛愬寲瀛樺偍锛屾瘡鏉¤褰曞悓鏃跺寘鍚細
		1. **Index Data**: 鐢ㄤ簬璁＄畻鐩镐技搴︾殑 Dense Vector 鍜?Sparse Vector銆?
		2. **Payload Data**: 瀹屾暣鐨?Chunk 鍘熷鏂囨湰 (Content) 鍙?Metadata銆?
		**鏈哄埗浼樺娍**锛氱‘淇濇绱㈠懡涓?ID 鍚庤兘绔嬪嵆鍙栧洖瀵瑰簲鐨勬鏂囧唴瀹癸紝鏃犻渶棰濆鐨勬煡搴撴搷浣?(Lookup)锛屼繚闅滀簡 Retrieve 闃舵鐨勬绉掔骇鍝嶅簲銆?
- **骞傜瓑鎬ц璁?(Idempotency)**锛?
		- 涓烘瘡涓?Chunk 鐢熸垚鍏ㄥ眬鍞竴鐨?`chunk_id`锛岀敓鎴愮畻娉曢噰鐢ㄧ‘瀹氱殑鍝堝笇缁勫悎锛歚hash(source_path + section_path + content_hash)`銆?
		- 鍐欏叆鏃堕噰鐢?"Upsert"锛堟洿鏂版垨鎻掑叆锛夎涔夛紝纭繚鍚屼竴鏂囨。鍗充娇琚娆″鐞嗭紝鏁版嵁搴撲腑涔熸案杩滃彧鏈変竴浠芥渶鏂板壇鏈紝褰诲簳閬垮厤閲嶅绱㈠紩闂銆?
	- **鍘熷瓙鎬т繚璇?*锛氫互 Batch 涓哄崟浣嶈繘琛屼簨鍔℃€у啓鍏ワ紝纭繚绱㈠紩鐘舵€佺殑涓€鑷存€с€?

- **鏂囨。鐢熷懡鍛ㄦ湡绠＄悊 (Document Lifecycle Management)**

	涓烘敮鎸?Dashboard 绠＄悊闈㈡澘涓殑鏂囨。娴忚涓庡垹闄ゅ姛鑳斤紝Ingestion 灞傞渶瑕佹彁渚涘畬鏁寸殑鏂囨。鐢熷懡鍛ㄦ湡绠＄悊鑳藉姏锛?

	- **DocumentManager锛堟枃妗ｇ鐞嗗櫒锛?*锛氱嫭绔嬩簬 Pipeline 鐨勬枃妗ｇ鐞嗘ā鍧楋紙`src/ingestion/document_manager.py`锛夛紝璐熻矗璺ㄥ瓨鍌ㄧ殑鍗忚皟鎿嶄綔锛?
		- `list_documents(collection?) -> List[DocumentInfo]`锛氬垪鍑哄凡鎽勫叆鏂囨。鍙婂叾缁熻淇℃伅锛坈hunk 鏁般€佸浘鐗囨暟銆佹憚鍏ユ椂闂达級銆?
		- `get_document_detail(doc_id) -> DocumentDetail`锛氳幏鍙栧崟涓枃妗ｇ殑璇︾粏淇℃伅锛堟墍鏈?chunk 鍐呭銆乵etadata銆佸叧鑱斿浘鐗囷級銆?
		- `delete_document(source_path, collection) -> DeleteResult`锛氬崗璋冨垹闄よ法 4 涓瓨鍌ㄧ殑鍏宠仈鏁版嵁锛?
			1. **Chroma** 鈥?鎸?`metadata.source` 鍒犻櫎鎵€鏈?chunk 鍚戦噺
			2. **BM25 Indexer** 鈥?绉婚櫎瀵瑰簲鏂囨。鐨勫€掓帓绱㈠紩鏉＄洰
			3. **ImageStorage** 鈥?鍒犻櫎璇ユ枃妗ｅ叧鑱旂殑鎵€鏈夊浘鐗囨枃浠?
			4. **FileIntegrity** 鈥?绉婚櫎澶勭悊璁板綍锛屼娇鏂囦欢鍙噸鏂版憚鍏?
		- `get_collection_stats(collection?) -> CollectionStats`锛氳繑鍥為泦鍚堢骇缁熻锛堟枃妗ｆ暟銆乧hunk 鏁般€佸瓨鍌ㄥぇ灏忕瓑锛夈€?

	- **Pipeline 杩涘害鍥炶皟 (Progress Callback)**锛氬湪 `IngestionPipeline.run()` 鏂规硶涓柊澧炲彲閫?`on_progress` 鍙傛暟锛?
		```python
		def run(self, source_path: str, collection: str = "default",
		        on_progress: Callable[[str, int, int], None] | None = None) -> IngestionResult:
		```
		- 鍥炶皟绛惧悕锛歚on_progress(stage_name: str, current: int, total: int)`
		- 鍚勯樁娈碉紙load / split / transform / embed / upsert锛夊湪澶勭悊姣忎釜 batch 鏃惰皟鐢ㄥ洖璋冿紝Dashboard 鎹灞曠ず瀹炴椂杩涘害鏉°€?
		- `on_progress` 涓?`None` 鏃惰涓轰笌褰撳墠瀹屽叏涓€鑷达紝涓嶅奖鍝?CLI 鍜屾祴璇曞満鏅€?

	- **瀛樺偍灞傛帴鍙ｆ墿灞?*锛氫负鏀寔 DocumentManager 鐨勫垹闄ゆ搷浣滐紝闇€鎵╁睍浠ヤ笅瀛樺偍鎺ュ彛锛?
		- `BaseVectorStore` 鏂板 `delete_by_metadata(filter: dict) -> int` 鈥?鎸?metadata 鏉′欢鎵归噺鍒犻櫎
		- `BM25Indexer` 鏂板 `remove_document(source: str) -> None` 鈥?绉婚櫎鎸囧畾鏂囨。鐨勭储寮曟潯鐩?
		- `FileIntegrityChecker` 鏂板 `remove_record(file_hash: str) -> None` 鍜?`list_processed() -> List[dict]`

#### 3.1.2 妫€绱㈡祦姘寸嚎


鏈ā鍧楀疄鐜版牳蹇冪殑 RAG 妫€绱㈠紩鎿庯紝閲囩敤 **鈥滃闃舵杩囨护 (Multi-stage Filtering)鈥?* 鏋舵瀯锛岃礋璐ｆ帴鏀跺凡娑堟鐨勭嫭绔嬫煡璇紙Standalone Query锛夛紝骞剁簿鍑嗗彫鍥?Top-K 鏈€鐩稿叧鐗囨銆?

- **Query Processing (鏌ヨ棰勫鐞?**
	- **鏍稿績鍋囪**锛氳緭鍏?Query 宸茬敱涓婃父锛圕lient/MCP Host锛夊畬鎴愪細璇濅笂涓嬫枃琛ュ叏锛圖e-referencing锛夛紝涓嶄粎濡傛锛岃繕杩涜浜嗘寚浠ｆ秷姝с€?
	- **鏌ヨ杞崲 (Transformation) 涓庢墿寮犵瓥鐣?(Expansion Strategy)**锛?
		- **Keyword Extraction**锛氬埄鐢?NLP 宸ュ叿鎻愬彇 Query 涓殑鍏抽敭瀹炰綋涓庡姩璇嶏紙鍘诲仠鐢ㄨ瘝锛夛紝鐢熸垚鐢ㄤ簬绋€鐤忔绱㈢殑 Token 鍒楄〃銆?
		- **Query Expansion **锛?
			- 绯荤粺鍙仛 Synonym/Alias Expansion锛堝悓涔夎瘝/鍒悕/缂╁啓鎵╁睍锛夛紝榛樿绛栫暐閲囩敤鈥?*鎵╁睍铻嶅叆绋€鐤忔绱€佺瀵嗘绱繚鎸佸崟娆?*鈥濅互鎺у埗鎴愭湰涓庡鏉傚害銆?
			- **Sparse Route (BM25)**锛氬皢鈥滃叧閿瘝 + 鍚屼箟璇?鍒悕鈥濆悎骞朵负涓€涓煡璇㈣〃杈惧紡锛堥€昏緫涓婃寜 `OR` 鎵╁睍锛夛紝**鍙墽琛屼竴娆＄█鐤忔绱?*銆傚師濮嬪叧閿瘝鍙祴浜堟洿楂樻潈閲嶄互鎶戝埗璇箟婕傜Щ銆?
			- **Dense Route (Embedding)**锛氫娇鐢ㄥ師濮?query锛堟垨杞诲害鏀瑰啓鍚庣殑璇箟 query锛夌敓鎴?embedding锛?*鍙墽琛屼竴娆＄瀵嗘绱?*锛涢粯璁や笉涓烘瘡涓悓涔夎瘝鍗曠嫭瑙﹀彂棰濆鐨勫悜閲忔绱㈣姹傘€?

- **Hybrid Search Execution (鍙岃矾娣峰悎妫€绱?**
	- **骞惰鍙洖 (Parallel Execution)**锛?
		- **Dense Route**锛氳绠?Query Embedding -> 妫€绱㈠悜閲忓簱锛圕osine Similarity锛?> 杩斿洖 Top-N 璇箟鍊欓€夈€?
		- **Sparse Route**锛氫娇鐢?BM25 绠楁硶 -> 妫€绱㈠€掓帓绱㈠紩 -> 杩斿洖 Top-N 鍏抽敭璇嶅€欓€夈€?
	- **缁撴灉铻嶅悎 (Fusion)**锛?
		- 閲囩敤 **RRF (Reciprocal Rank Fusion)** 绠楁硶锛屼笉渚濊禆鍚勮矾鍒嗘暟鐨勭粷瀵瑰€硷紝鑰屾槸鍩轰簬鎺掑悕鐨勫€掓暟杩涜鍔犳潈铻嶅悎銆?
		- 鍏紡绛栫暐锛歚Score = 1 / (k + Rank_Dense) + 1 / (k + Rank_Sparse)`锛屽钩婊戝洜鍗曚竴妯℃€佺己闄峰鑷寸殑婕忓彫鍥炪€?

- **Filtering & Reranking (绮剧‘杩囨护涓庨噸鎺?**
	- **Metadata Filtering Strategy (閫氱敤杩囨护绛栫暐)**锛?
		- **鍘熷垯锛氬厛瑙ｆ瀽銆佽兘鍓嶇疆鍒欏墠缃€佹棤娉曞墠缃垯鍚庣疆鍏滃簳銆?*
		- Query Processing 闃舵搴斿皢缁撴瀯鍖栫害鏉熻В鏋愪负閫氱敤 `filters`锛堜緥濡?`collection`/`doc_type`/`language`/`time_range`/`access_level` 绛夛級銆?
		- 鑻ュ簳灞傜储寮曟敮鎸佷笖灞炰簬纭害鏉燂紙Hard Filter锛夛紝鍒欏湪 Dense/Sparse 妫€绱㈤樁娈靛仛 Pre-filter 浠ョ缉灏忓€欓€夐泦銆侀檷浣庢垚鏈€?
		- 鏃犳硶鍓嶇疆鐨勮繃婊わ紙绱㈠紩涓嶆敮鎸佹垨瀛楁缂哄け/璐ㄩ噺涓嶇ǔ锛夊湪 Rerank 鍓嶇粺涓€鍋?Post-filter 浣滀负 safety net锛涘缂哄け瀛楁榛樿閲囧彇鈥滃鏉惧寘鍚€?missing->include) 浠ラ伩鍏嶈鏉€鍙洖銆?
		- 杞亸濂斤紙Soft Preference锛屼緥濡傗€滄洿杩戞湡鏇村ソ鈥濓級涓嶅簲纭繃婊わ紝鑰屽簲浣滀负鎺掑簭淇″彿鍦ㄨ瀺鍚?閲嶆帓闃舵鍔犳潈銆?
	- **Rerank Backend (鍙彃鎷旂簿鎺掑悗绔?**锛?
		- **鐩爣**锛氬湪 Top-M 鍊欓€変笂杩涜楂樼簿搴︽帓搴?杩囨护锛涜妯″潡蹇呴』鍙叧闂紝骞舵彁渚涚ǔ瀹氬洖閫€绛栫暐銆?
		- **鍚庣閫夐」**锛?
			1. **None (鍏抽棴绮炬帓)**锛氱洿鎺ヨ繑鍥炶瀺鍚堝悗鐨?Top-K锛圧RF 鎺掑悕浣滀负鏈€缁堢粨鏋滐級銆?
			2. **Cross-Encoder Rerank (鏈湴/鎵樼妯″瀷)**锛氳緭鍏ヤ负 `[Query, Chunk]` 瀵癸紝杈撳嚭鐩稿叧鎬у垎鏁板苟鎺掑簭锛涢€傚悎绋冲畾銆佺粨鏋勫寲杈撳嚭銆侰PU 鐜涓嬪缓璁粯璁や粎瀵硅緝灏忕殑 Top-M 鎵ц锛堜緥濡?M=10~30锛夛紝骞舵彁渚涜秴鏃跺洖閫€銆?
			3. **LLM Rerank (鍙€?**锛氫娇鐢?LLM 瀵瑰€欓€夐泦鎺掑簭/閫夋嫨锛涢€傚悎闇€瑕佹洿寮烘寚浠ょ悊瑙ｆ垨鏃犳湰鍦版ā鍨嬬幆澧冩椂銆備负鎺у埗鎴愭湰涓庣ǔ瀹氭€э紝鍊欓€夋暟搴旀洿灏忥紙渚嬪 M<=20锛夛紝骞惰姹傝緭鍑轰弗鏍肩粨鏋勫寲鏍煎紡锛堝 JSON 鐨?ranked ids锛夈€?
		- **榛樿涓庡洖閫€ (Fallback)**锛?
			- 榛樿绛栫暐闈㈠悜閫氱敤妗嗘灦涓?CPU 鐜锛氫紭鍏堜繚璇佲€滃彲鐢ㄤ笌鍙帶鈥濓紝Cross-Encoder/LLM 鍧囦负鍙€夊寮恒€?
			- 褰撶簿鎺掍笉鍙敤/瓒呮椂/澶辫触鏃讹紝蹇呴』鍥為€€鍒拌瀺鍚堥樁娈电殑鎺掑簭锛圧RF Top-K锛夛紝纭繚绯荤粺鍙敤鎬т笌缁撴灉绋冲畾鎬с€?

### 3.2 MCP 鏈嶅姟璁捐 (MCP Service Design)

**鐩爣锛?* 璁捐骞跺疄鐜颁竴涓鍚?Model Context Protocol (MCP) 瑙勮寖鐨?Server锛屼娇鍏惰兘澶熶綔涓虹煡璇嗕笂涓嬫枃鎻愪緵鑰咃紝鏃犵紳瀵规帴涓绘祦 MCP Clients锛堝 GitHub Copilot銆丆laude Desktop 绛夛級锛岃鐢ㄦ埛閫氳繃鐜版湁 AI 鍔╂墜鍗冲彲鏌ヨ绉佹湁鐭ヨ瘑搴撱€?

#### 3.2.1 鏍稿績璁捐鐞嗗康

- **鍗忚浼樺厛 (Protocol-First)**锛氫弗鏍奸伒寰?MCP 瀹樻柟瑙勮寖锛圝SON-RPC 2.0锛夛紝纭繚涓庝换浣曞悎瑙?Client 鐨勪簰鎿嶄綔鎬с€?
- **寮€绠卞嵆鐢?(Zero-Config for Clients)**锛欳lient 绔棤闇€浠讳綍鐗规畩閰嶇疆锛屽彧闇€鍦ㄩ厤缃枃浠朵腑娣诲姞 Server 杩炴帴淇℃伅鍗冲彲浣跨敤鍏ㄩ儴鍔熻兘銆?
- **寮曠敤閫忔槑 (Citation Transparency)**锛氭墍鏈夋绱㈢粨鏋滃繀椤绘惡甯﹀畬鏁寸殑鏉ユ簮淇℃伅锛屾敮鎸?Client 绔睍绀?鍥炵瓟渚濇嵁"锛屽寮虹敤鎴峰 AI 杈撳嚭鐨勪俊浠汇€?
- **澶氭ā鎬佸弸濂?(Multimodal-Ready)**锛氳繑鍥炴牸寮忓簲鏀寔鏂囨湰涓庡浘鍍忕瓑澶氱鍐呭绫诲瀷锛屼负鏈潵鐨勫瘜濯掍綋灞曠ず棰勭暀鎵╁睍绌洪棿銆?

#### 3.2.2 浼犺緭鍗忚锛歋tdio 鏈湴閫氫俊

鏈」鐩噰鐢?**Stdio Transport** 浣滀负鍞竴閫氫俊妯″紡銆?

- **宸ヤ綔鏂瑰紡**锛欳lient锛圴S Code Copilot銆丆laude Desktop锛変互瀛愯繘绋嬫柟寮忓惎鍔ㄦ垜浠殑 Server锛屽弻鏂归€氳繃鏍囧噯杈撳叆/杈撳嚭浜ゆ崲 JSON-RPC 娑堟伅銆?
- **閫夊瀷鐞嗙敱**锛?
	- **闆堕厤缃?*锛氭棤闇€缃戠粶绔彛銆佹棤闇€閴存潈锛岀敤鎴峰彧闇€鍦?Client 閰嶇疆鏂囦欢涓寚瀹氬惎鍔ㄥ懡浠ゅ嵆鍙娇鐢ㄣ€?
	- **闅愮瀹夊叏**锛氭暟鎹笉缁忚繃缃戠粶锛屽ぉ鐒堕€傚悎澶勭悊绉佹湁鐭ヨ瘑搴撲笌鏁忔劅涓氬姟鏁版嵁銆?
	- **濂戝悎瀹氫綅**锛歋tdio 瀹岀編閫傞厤寮€鍙戣€呮湰鍦板伐浣滄祦锛屾弧瓒崇鏈夌煡璇嗙鐞嗕笌蹇€熷師鍨嬮獙璇侀渶姹傘€?
- **瀹炵幇绾︽潫**锛?
	- `stdout` 浠呰緭鍑哄悎娉?MCP 娑堟伅锛岀姝㈡贩鍏ヤ换浣曟棩蹇楁垨璋冭瘯淇℃伅銆?
	- 鏃ュ織缁熶竴杈撳嚭鑷?`stderr`锛岄伩鍏嶆薄鏌撻€氫俊閫氶亾銆?

#### 3.2.3 SDK 涓庡疄鐜板簱閫夊瀷

- **棣栭€夛細Python 瀹樻柟 MCP SDK (`mcp`)**
	- **浼樺娍**锛?
		- 瀹樻柟缁存姢锛屼笌鍗忚瑙勮寖鍚屾鏇存柊锛屼繚璇佹渶鏂扮壒鎬ф敮鎸侊紙濡?`outputSchema`銆乣annotations` 绛夛級銆?
		- 鎻愪緵 `@server.tool()` 绛夎楗板櫒锛屽０鏄庡紡瀹氫箟 Tools/Resources/Prompts锛屼唬鐮佺畝娲併€?
		- 鍐呯疆 Stdio 涓?HTTP Transport 鏀寔锛屾棤闇€鎵嬪姩澶勭悊 JSON-RPC 搴忓垪鍖栦笌鐢熷懡鍛ㄦ湡绠＄悊銆?
	- **閫傜敤**锛氭湰椤圭洰鐨勯粯璁ゅ疄鐜版柟妗堛€?

- **澶囬€夛細FastAPI + 鑷畾涔夊崗璁眰**
	- **鍦烘櫙**锛氶渶瑕佹繁搴﹀畾鍒?HTTP 琛屼负锛堝鑷畾涔変腑闂翠欢銆佸鏉傞壌鏉冩祦绋嬶級鎴栧笇鏈涘涔?MCP 鍗忚搴曞眰缁嗚妭鏃跺彲鑰冭檻銆?
	- **鏉冭　**锛氬紑鍙戞垚鏈洿楂橈紝闇€鑷瀹炵幇鑳藉姏鍗忓晢 (Capability Negotiation)銆侀敊璇爜鏄犲皠绛夛紝涓旈渶鎸佺画璺熻繘鍗忚鐗堟湰鏇存柊銆?

- **鍗忚鐗堟湰**锛氳窡韪?MCP 鏈€鏂扮ǔ瀹氱増鏈紙濡?`2025-06-18`锛夛紝鍦?`initialize` 闃舵杩涜鐗堟湰鍗忓晢锛岀‘淇?Client/Server 鍏煎鎬с€?

#### 3.2.4 瀵瑰鏆撮湶鐨勫伐鍏峰嚱鏁拌璁?(Tools Design)

Server 閫氳繃 `tools/list` 鍚?Client 娉ㄥ唽鍙皟鐢ㄧ殑宸ュ叿鍑芥暟銆傚伐鍏疯璁″簲閬靛惊"鍗曚竴鑱岃矗銆佸弬鏁版槑纭€佽緭鍑轰赴瀵?鍘熷垯銆?

- **鏍稿績宸ュ叿闆?*锛?

| 宸ュ叿鍚嶇О | 鍔熻兘鎻忚堪 | 鍏稿瀷杈撳叆鍙傛暟 | 杈撳嚭鐗圭偣 |
|---------|---------|-------------|---------|
| `query_knowledge_hub` | 涓绘绱㈠叆鍙ｏ紝鎵ц娣峰悎妫€绱?+ Rerank锛岃繑鍥炴渶鐩稿叧鐗囨 | `query: string`, `top_k?: int`, `collection?: string` | 杩斿洖甯﹀紩鐢ㄧ殑缁撴瀯鍖栫粨鏋?|
| `list_collections` | 鍒椾妇鐭ヨ瘑搴撲腑鍙敤鐨勬枃妗ｉ泦鍚?| 鏃?| 闆嗗悎鍚嶇О銆佹弿杩般€佹枃妗ｆ暟閲?|
| `get_document_summary` | 鑾峰彇鎸囧畾鏂囨。鐨勬憳瑕佷笌鍏冧俊鎭?| `doc_id: string` | 鏍囬銆佹憳瑕併€佸垱寤烘椂闂淬€佹爣绛?|

- **鎵╁睍宸ュ叿锛圓gentic 婕旇繘鏂瑰悜锛?*锛?
	- `search_by_keyword` / `search_by_semantic`锛氭媶鍒嗙嫭绔嬬殑妫€绱㈢瓥鐣ワ紝渚?Agent 鑷富閫夋嫨銆?
	- `verify_answer`锛氫簨瀹炴牳鏌ュ伐鍏凤紝妫€娴嬬敓鎴愬唴瀹规槸鍚︽湁渚濇嵁鏀拺銆?
	- `list_document_sections`锛氭祻瑙堟枃妗ｇ洰褰曠粨鏋勶紝鏀寔澶氭瀵艰埅寮忔绱€?

#### 3.2.5 杩斿洖鍐呭涓庡紩鐢ㄩ€忔槑璁捐 (Response & Citation Design)

MCP 鍗忚鐨?Tool 杩斿洖鏍煎紡鏀寔澶氱鍐呭绫诲瀷锛坄content` 鏁扮粍锛夛紝鏈」鐩皢鍏呭垎鍒╃敤杩欎竴鐗规€у疄鐜?鍙函婧?鐨勫洖绛旓細

- **缁撴瀯鍖栧紩鐢ㄨ璁?*锛?
	- 姣忎釜妫€绱㈢粨鏋滅墖娈靛簲鍖呭惈瀹屾暣鐨勫畾浣嶄俊鎭細`source_file`锛堟枃浠跺悕/璺緞锛夈€乣page`锛堥〉鐮侊紝濡傞€傜敤锛夈€乣chunk_id`锛堢墖娈垫爣璇嗭級銆乣score`锛堢浉鍏虫€у垎鏁帮級銆?
	- 鎺ㄨ崘鍦ㄨ繑鍥炵殑 `structuredContent` 涓噰鐢ㄧ粺涓€鐨?Citation 鏍煎紡锛?
		```
		{
		  "answer": "...",
		  "citations": [
		    { "id": 1, "source": "xxx.pdf", "page": 5, "text": "鍘熸枃鐗囨...", "score": 0.92 },
		    ...
		  ]
		}
		```
	- 鍚屾椂鍦?`content` 鏁扮粍涓互 Markdown 鏍煎紡鍛堢幇浜虹被鍙鐨勫甫寮曠敤鍥炵瓟锛坄[1]` 鏍囨敞锛夛紝淇濊瘉 Client 鏃犺鏄惁瑙ｆ瀽缁撴瀯鍖栧唴瀹归兘鑳藉睍绀哄紩鐢ㄣ€?

- **澶氭ā鎬佸唴瀹硅繑鍥?*锛?
	- **鏂囨湰鍐呭 (TextContent)**锛氶粯璁よ繑鍥炵被鍨嬶紝Markdown 鏍煎紡锛屾敮鎸佷唬鐮佸潡銆佸垪琛ㄧ瓑瀵屾枃鏈€?
	- **鍥惧儚鍐呭 (ImageContent)**锛氬綋妫€绱㈢粨鏋滃叧鑱斿浘鍍忔椂锛孲erver 璇诲彇鏈湴鍥剧墖鏂囦欢骞剁紪鐮佷负 Base64 杩斿洖銆?
		- **鏍煎紡**锛歚{ "type": "image", "data": "<base64>", "mimeType": "image/png" }`
		- **宸ヤ綔娴佺▼**锛氭暟鎹憚鍙栭樁娈靛瓨鍌ㄥ浘鐗囨湰鍦拌矾寰?鈫?妫€绱㈠懡涓悗 Server 鍔ㄦ€佽鍙?鈫?缂栫爜涓?Base64 鈫?宓屽叆杩斿洖娑堟伅銆?
		- **Client 鍏煎鎬?*锛氬浘鍍忓睍绀鸿兘鍔涘彇鍐充簬 Client 瀹炵幇锛孏itHub Copilot 鍙兘闄嶇骇澶勭悊锛孋laude Desktop 鏀寔瀹屾暣娓叉煋銆係erver 绔粺涓€杩斿洖 Base64 鏍煎紡锛岀敱 Client 鍐冲畾濡備綍娓叉煋銆?

- **Client 閫傞厤绛栫暐**锛?
	- **GitHub Copilot (VS Code)**锛氬綋鍓嶅 MCP 鐨勬敮鎸侀泦涓湪 Tools 璋冪敤锛岃繑鍥炵殑 `content` 涓殑鏂囨湰浼氬睍绀虹粰鐢ㄦ埛銆傚缓璁互娓呮櫚鐨?Markdown 鏂囨湰锛堝惈寮曠敤鏍囨敞锛変负涓伙紝鍥惧儚浣滀负琛ュ厖銆?
	- **Claude Desktop**锛氬 MCP Tools/Resources 鏈夊畬鏁存敮鎸侊紝鍥惧儚涓庤祫婧愰摼鎺ュ彲鐩存帴娓叉煋銆傚彲鏇存縺杩涘湴浣跨敤澶氭ā鎬佽繑鍥炪€?
	- **閫氱敤鍏煎鍘熷垯**锛氬缁堝湪 `content` 鏁扮粍绗竴椤规彁渚涚函鏂囨湰/Markdown 鐗堟湰鐨勭瓟妗堬紝纭繚鏈€浣庡吋瀹规€э紱灏嗙粨鏋勫寲鏁版嵁銆佸浘鍍忕瓑鏀惧湪鍚庣画椤规垨 `structuredContent` 涓紝渚涢珮绾?Client 瑙ｆ瀽銆?

### 3.3 鍙彃鎷旀灦鏋勮璁?(Pluggable Architecture Design)

**鐩爣锛?* 瀹氫箟娓呮櫚鐨勬娊璞″眰涓庢帴鍙ｅ绾︼紝浣?RAG 閾捐矾鐨勬瘡涓牳蹇冪粍浠堕兘鑳藉鐙珛鏇挎崲涓庡崌绾э紝閬垮厤鎶€鏈攣瀹氾紝鏀寔浣庢垚鏈殑 A/B 娴嬭瘯涓庣幆澧冭縼绉汇€?

> **鏈璇存槑**锛氭湰鑺備腑鐨?鎻愪緵鑰?(Provider)"銆?瀹炵幇 (Implementation)"鎸囩殑鏄畬鎴愭煇椤瑰姛鑳界殑**鍏蜂綋鎶€鏈柟妗?*锛岃€岄潪浼犵粺 Web 鏋舵瀯涓殑"鍚庣鏈嶅姟鍣?銆備緥濡傦紝LLM 鎻愪緵鑰呭彲浠ユ槸杩滅▼鐨?Azure OpenAI API锛屼篃鍙互鏄湰鍦拌繍琛岀殑 Ollama锛涘悜閲忓瓨鍌ㄥ彲浠ユ槸鏈湴宓屽叆寮忕殑 Chroma锛屼篃鍙互鏄簯绔墭绠＄殑 Pinecone銆傛湰椤圭洰浣滀负鏈湴 MCP Server锛岄€氳繃缁熶竴鎺ュ彛瀵规帴杩欎簺涓嶅悓鐨勬彁渚涜€咃紝瀹炵幇鐏垫椿鍒囨崲銆?

#### 3.3.1 璁捐鍘熷垯

- **鎺ュ彛闅旂 (Interface Segregation)**锛氫负姣忕被缁勪欢瀹氫箟鏈€灏忓寲鐨勬娊璞℃帴鍙ｏ紝涓婂眰涓氬姟閫昏緫浠呬緷璧栨帴鍙ｈ€岄潪鍏蜂綋瀹炵幇銆?
- **閰嶇疆椹卞姩 (Configuration-Driven)**锛氶€氳繃缁熶竴閰嶇疆鏂囦欢锛堝 `settings.yaml`锛夋寚瀹氬悇缁勪欢鐨勫叿浣撳悗绔紝浠ｇ爜鏃犻渶淇敼鍗冲彲鍒囨崲瀹炵幇銆?
- **宸ュ巶妯″紡 (Factory Pattern)**锛氫娇鐢ㄥ伐鍘傚嚱鏁版牴鎹厤缃姩鎬佸疄渚嬪寲瀵瑰簲鐨勫疄鐜扮被锛屽疄鐜?涓€澶勯厤缃紝澶勫鐢熸晥"銆?
- **浼橀泤闄嶇骇 (Graceful Fallback)**锛氬綋棣栭€夊悗绔笉鍙敤鏃讹紝绯荤粺搴旇嚜鍔ㄥ洖閫€鍒板閫夋柟妗堟垨瀹夊叏榛樿鍊硷紝淇濋殰鍙敤鎬с€?

**閫氱敤缁撴瀯绀烘剰锛堥€傜敤浜?3.3.2 / 3.3.3 / 3.3.4 绛夊彲鎻掓嫈缁勪欢锛?*锛?

```
涓氬姟浠ｇ爜
  鈹?
  鈻?
<Component>Factory.get_xxx()  鈫?璇诲彇閰嶇疆锛屽喅瀹氱敤鍝釜瀹炵幇
  鈹?
  鈹溾攢鈫?ImplementationA()
  鈹溾攢鈫?ImplementationB()  
  鈹斺攢鈫?ImplementationC()
      鈹?
      鈻?
    閮藉疄鐜颁簡缁熶竴鐨勬娊璞℃帴鍙?
```

#### 3.3.2 LLM 涓?Embedding 鎻愪緵鑰呮娊璞?

杩欐槸鍙彃鎷旇璁＄殑鏍稿績鐜妭锛屽洜涓烘ā鍨嬫彁渚涜€呯殑閫夋嫨鐩存帴褰卞搷鎴愭湰銆佹€ц兘涓庨殣绉佸悎瑙勩€?

- **缁熶竴鎺ュ彛灞?(Unified API Abstraction)**锛?
	- **璁捐鎬濊矾**锛氭棤璁哄簳灞備娇鐢?Azure OpenAI銆丱penAI 鍘熺敓 API銆丏eepSeek 杩樻槸鏈湴 Ollama锛屼笂灞傝皟鐢ㄤ唬鐮佸簲淇濇寔涓€鑷淬€?
	- **鍏抽敭鎶借薄**锛?
		- `LLMClient`锛氭毚闇?`chat(messages) -> response` 鏂规硶锛屽睆钄戒笉鍚?Provider 鐨勮璇佹柟寮忎笌璇锋眰鏍煎紡宸紓銆?
		- `EmbeddingClient`锛氭毚闇?`embed(texts) -> vectors` 鏂规硶锛岀粺涓€澶勭悊鎵归噺璇锋眰涓庣淮搴﹀綊涓€鍖栥€?

- **鎻愪緵鑰呴€夐」涓庡垏鎹㈠満鏅?*锛?

| 鎻愪緵鑰呯被鍨?| 鍏稿瀷鍦烘櫙 | 閰嶇疆鍒囨崲鐐?|
|---------|---------|-----------|
| **Azure OpenAI** | 浼佷笟鍚堣銆佺鏈変簯閮ㄧ讲銆佸尯鍩熸暟鎹┗鐣?| `provider: azure`, `endpoint`, `api_key`, `deployment_name` |
| **OpenAI 鍘熺敓** | 閫氱敤寮€鍙戙€佹渶鏂版ā鍨嬪皾椴?| `provider: openai`, `api_key`, `model` |
| **DeepSeek / 鍏朵粬浜戠** | 鎴愭湰浼樺寲銆佺壒瀹氳瑷€浼樺寲 | `provider: deepseek`, `api_key`, `model` |
| **Ollama / vLLM (鏈湴)** | 瀹屽叏绂荤嚎銆侀殣绉佹晱鎰熴€佹棤 API 鎴愭湰 | `provider: ollama`, `base_url`, `model` |

- **鎶€鏈€夊瀷寤鸿**锛?
	- 鏈」鐩噰鐢ㄨ嚜鐮旂殑 `BaseLLM` / `BaseEmbedding` 鎶借薄鍩虹被锛岄厤鍚堝伐鍘傛ā寮忥紙`llm_factory.py` / `embedding_factory.py`锛夊疄鐜扮粺涓€璋冪敤鎺ュ彛銆傚凡鍐呯疆 Azure OpenAI銆丱penAI銆丱llama銆丏eepSeek 鍥涚 Provider 閫傞厤銆?
	- 瀵逛簬鍏朵粬 Provider锛屽彲閫氳繃 **OpenAI-Compatible 妯″紡**鎺ュ叆锛堣缃嚜瀹氫箟 `api_base`锛夛紝鎴栧疄鐜?`BaseLLM` 鎺ュ彛骞跺湪宸ュ巶涓敞鍐屻€?

	- 瀵逛簬浼佷笟绾ч渶姹傦紝鍙湪鍏跺熀纭€涓婂鍔犵粺涓€鐨?**閲嶈瘯銆侀檺娴併€佹棩蹇?* 涓棿灞傦紝鎻愬崌鐢熶骇鍙潬鎬э紝浣嗘湰椤圭洰鏆備笉瀹炵幇锛岃繖閲屼粎鎻愪緵鎬濊矾銆?
	- **Vision LLM 鎵╁睍**锛氶拡瀵瑰浘鍍忔弿杩扮敓鎴愶紙Image Captioning锛夐渶姹傦紝绯荤粺鎵╁睍浜?`BaseVisionLLM` 鎺ュ彛锛屾敮鎸佹枃鏈?鍥剧墖鐨勫妯℃€佽緭鍏ャ€傚綋鍓嶅疄鐜帮細
		- **Azure OpenAI Vision**锛圙PT-4o/GPT-4-Vision锛夛細浼佷笟绾у悎瑙勯儴缃诧紝鏀寔澶嶆潅鍥捐〃瑙ｆ瀽锛屼笌 Azure 鐢熸€佹繁搴﹂泦鎴愩€?

#### 3.3.3 妫€绱㈢瓥鐣ユ娊璞?

妫€绱㈠眰鐨勫彲鎻掓嫈鎬у喅瀹氫簡绯荤粺鍦ㄤ笉鍚屾暟鎹妯′笌鏌ヨ妯″紡涓嬬殑閫傚簲鑳藉姏銆?

**璁捐妯″紡锛氭娊璞″伐鍘傛ā寮?*

涓?3.3.2 鑺傜殑 LLM 鎶借薄绫讳技锛屾绱㈠眰鍚勭粍浠剁殑鍙彃鎷旀€у悓鏍蜂緷璧栦袱灞傝璁★細

1. **鑷爺鐨勭粺涓€鎶借薄鎺ュ彛**锛氭湰椤圭洰涓哄悜閲忔暟鎹簱锛坄BaseVectorStore`锛夈€丒mbedding锛坄BaseEmbedding`锛夈€佸垎鍧楋紙`BaseSplitter`锛夌瓑鏍稿績缁勪欢瀹氫箟浜嗙粺涓€鐨勬娊璞″熀绫伙紝涓嶅悓瀹炵幇鍙渶閬靛惊鐩稿悓鎺ュ彛鍗冲彲鏃犵紳鏇挎崲銆?

2. **宸ュ巶鍑芥暟璺敱**锛氭瘡涓娊璞″眰閰嶅宸ュ巶鍑芥暟锛堝 `embedding_factory.py`銆乣splitter_factory.py`锛夛紝鏍规嵁 `settings.yaml` 涓殑閰嶇疆瀛楁鑷姩瀹炰緥鍖栧搴斿疄鐜帮紝瀹炵幇"鏀归厤缃笉鏀逛唬鐮?鐨勫垏鎹綋楠屻€?


閫氱敤鐨勨€滈厤缃┍鍔?+ 宸ュ巶璺敱鈥濈粨鏋勭ず鎰忚 3.3.1 鑺傘€?

涓嬮潰鍒嗗埆璇存槑鍚勭粍浠跺浣曞簲鐢ㄨ繖涓€妯″紡锛?

---

**1. 鍒嗗潡绛栫暐 (Chunking Strategy)**

鍒嗗潡鏄?Ingestion Pipeline 鐨勬牳蹇冪幆鑺備箣涓€锛屽喅瀹氫簡鏂囨。濡備綍琚垏鍒嗕负閫傚悎妫€绱㈢殑璇箟鍗曞厓銆傛湰椤圭洰鐨?Splitter 灞傞噰鐢ㄥ彲鎻掓嫈璁捐锛圔aseSplitter 鎶借薄鎺ュ彛 + SplitterFactory 宸ュ巶锛夛紝涓嶅悓鍒嗗潡瀹炵幇鍙渶閬靛惊鐩稿悓鎺ュ彛鍗冲彲鏃犵紳鏇挎崲銆?

甯歌鐨勫垎鍧楃瓥鐣ュ寘鎷細
- **鍥哄畾闀垮害鍒囧垎**锛氭寜瀛楃鏁版垨 Token 鏁板垏鍒嗭紝绠€鍗曚絾鍙兘鐮村潖璇箟瀹屾暣鎬с€?
- **閫掑綊瀛楃鍒囧垎**锛氭寜灞傜骇鍒嗛殧绗︼紙娈佃惤鈫掑彞瀛愨啋瀛楃锛夐€掑綊鍒囧垎锛屽湪闀垮害闄愬埗鍐呭敖閲忎繚鎸佽涔夎竟鐣屻€?
- **璇箟鍒囧垎**锛氬埄鐢?Embedding 鐩镐技搴︽娴嬭涔夋柇鐐癸紝纭繚姣忎釜 Chunk 鏄嚜鍖呭惈鐨勮涔夊崟鍏冦€?
- **缁撴瀯鎰熺煡鍒囧垎**锛氭牴鎹枃妗ｇ粨鏋勶紙Markdown 鏍囬銆佷唬鐮佸潡銆佸垪琛ㄧ瓑锛夎繘琛屽垏鍒嗐€?

鏈」鐩綋鍓嶉噰鐢?**LangChain 鐨?`RecursiveCharacterTextSplitter`** 杩涜鍒囧垎锛岃鏂规硶瀵?Markdown 鏂囨。鐨勭粨鏋勶紙鏍囬銆佹钀姐€佸垪琛ㄣ€佷唬鐮佸潡锛夋湁澶╃劧鐨勯€傞厤鎬э紝鑳藉閫氳繃閰嶇疆璇箟鏂偣锛圫eparators锛夊疄鐜伴珮璐ㄩ噺銆佽涔夊畬鏁寸殑鍒囧潡銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熶娇鐢?LangChain RecursiveCharacterTextSplitter銆傛灦鏋勮璁′笂棰勭暀浜嗗垏鎹㈣兘鍔涳紝濡傞渶鍒囨崲涓?SentenceSplitter銆丼emanticSplitter 鎴栬嚜瀹氫箟鍒囧垎鍣紝鍙渶瀹炵幇 BaseSplitter 鎺ュ彛骞跺湪閰嶇疆涓寚瀹氬嵆鍙€?

---

**2. 鍚戦噺鏁版嵁搴?(Vector Store)**

鏈」鐩嚜瀹氫箟浜嗙粺涓€鐨?BaseVectorStore 鎶借薄鎺ュ彛锛屾毚闇?.add()銆?query()銆?delete() 绛夋柟娉曘€傛墍鏈夊悜閲忔暟鎹簱鍚庣锛圕hroma銆丵drant銆丳inecone 绛夛級鍙渶瀹炵幇璇ユ帴鍙ｅ嵆鍙彃鎷旀浛鎹紝閫氳繃 VectorStoreFactory 鏍规嵁閰嶇疆鑷姩閫夋嫨鍏蜂綋瀹炵幇銆?

鏈」鐩€夌敤 **Chroma** 浣滀负鍚戦噺鏁版嵁搴撱€傜浉姣?Qdrant銆丮ilvus銆乄eaviate 绛夐渶瑕?Docker 瀹瑰櫒鎴栧垎甯冨紡鏋舵瀯鏀拺鐨勬柟妗堬紝Chroma 閲囩敤宓屽叆寮忚璁★紝`pip install chromadb` 鍗冲彲浣跨敤锛屾棤闇€棰濆閮ㄧ讲鏁版嵁搴撴湇鍔★紝闈炲父閫傚悎鏈湴寮€鍙戜笌蹇€熷師鍨嬮獙璇併€傚悓鏃?ChromaStore 閫傞厤鍣紙src/libs/vector_store/chroma_store.py锛夛紝涓?Pipeline 鏃犵紳闆嗘垚銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熶粎瀹炵幇浜?Chroma 鍚庣銆傝櫧鐒舵灦鏋勮璁′笂棰勭暀浜嗗伐鍘傛ā寮忎互鏀寔鏈潵鎵╁睍锛屼絾褰撳墠鐗堟湰灏氭湭瀹炵幇鍏朵粬鍚戦噺鏁版嵁搴撶殑閫傞厤鍣ㄣ€?

---

**3. 鍚戦噺缂栫爜绛栫暐 (Embedding Strategy)**

鍚戦噺缂栫爜鏄?Ingestion Pipeline 鐨勫叧閿幆鑺傦紝鍐冲畾浜?Chunk 濡備綍琚浆鎹负鍙绱㈢殑鍚戦噺琛ㄧず銆傛湰椤圭洰鑷畾涔変簡 BaseEmbedding 鎶借薄鎺ュ彛锛坰rc/libs/embedding/base.py锛夛紝鏀寔涓嶅悓 Embedding 妯″瀷鐨勫彲鎻掓嫈鏇挎崲銆?

甯歌鐨勭紪鐮佺瓥鐣ュ寘鎷細
- **绾瀵嗙紪鐮侊紙Dense Only锛?*锛氫粎鐢熸垚璇箟鍚戦噺锛岄€傚悎閫氱敤鍦烘櫙銆?
- **绾█鐤忕紪鐮侊紙Sparse Only锛?*锛氫粎鐢熸垚鍏抽敭璇嶆潈閲嶅悜閲忥紝閫傚悎绮剧‘鍖归厤鍦烘櫙銆?
- **鍙岃矾缂栫爜锛圖ense + Sparse锛?*锛氬悓鏃剁敓鎴愮瀵嗗悜閲忓拰绋€鐤忓悜閲忥紝涓烘贩鍚堟绱㈡彁渚涙暟鎹熀纭€銆?

鏈」鐩綋鍓嶉噰鐢?**鍙岃矾缂栫爜锛圖ense + Sparse锛?* 绛栫暐锛?
- **Dense Embeddings锛堣涔夊悜閲忥級**锛氳皟鐢?Embedding 妯″瀷锛堝 OpenAI text-embedding-3锛夌敓鎴愰珮缁存诞鐐瑰悜閲忥紝鎹曟崏鏂囨湰鐨勬繁灞傝涔夊叧鑱斻€?
- **Sparse Embeddings锛堢█鐤忓悜閲忥級**锛氬埄鐢?BM25 缂栫爜鍣ㄧ敓鎴愮█鐤忓悜閲忥紙Keyword Weights锛夛紝鎹曟崏绮剧‘鐨勫叧閿瘝鍖归厤淇℃伅銆?

瀛樺偍鏃讹紝Dense Vector 鍜?Sparse Vector 涓?Chunk 鍘熸枃銆丮etadata 涓€璧峰師瀛愬寲鍐欏叆鍚戦噺鏁版嵁搴擄紝纭繚妫€绱㈡椂鍙悓鏃跺埄鐢ㄤ袱绉嶅悜閲忋€?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熷疄鐜颁簡 Dense + Sparse 鍙岃矾缂栫爜銆傛灦鏋勮璁′笂棰勭暀浜嗗垏鎹㈣兘鍔涳紝濡傞渶浣跨敤鍏朵粬 Embedding 妯″瀷锛堝 BGE銆丱llama 鏈湴妯″瀷锛夋垨璋冩暣缂栫爜绛栫暐锛屽彲鍦?Pipeline 涓浛鎹㈢浉搴旂粍浠躲€?

---

**4. 鍙洖绛栫暐 (Retrieval Strategy)**

鍙洖绛栫暐鍐冲畾浜嗘煡璇㈤樁娈靛浣曚粠鐭ヨ瘑搴撲腑妫€绱㈢浉鍏冲唴瀹广€傚熀浜?Ingestion 闃舵瀛樺偍鐨勫悜閲忕被鍨嬶紝鍙噰鐢ㄤ笉鍚岀殑鍙洖鏂规锛?
- **绾瀵嗗彫鍥烇紙Dense Only锛?*锛氫粎浣跨敤璇箟鍚戦噺杩涜鐩镐技搴﹀尮閰嶃€?
- **绾█鐤忓彫鍥烇紙Sparse Only锛?*锛氫粎浣跨敤 BM25 杩涜鍏抽敭璇嶅尮閰嶃€?
- **娣峰悎鍙洖锛圚ybrid锛?*锛氬苟琛屾墽琛岀瀵嗗拰绋€鐤忎袱璺彫鍥烇紝鍐嶉€氳繃铻嶅悎绠楁硶鍚堝苟缁撴灉銆?
- **娣峰悎鍙洖 + 绮炬帓锛圚ybrid + Rerank锛?*锛氬湪娣峰悎鍙洖鍩虹涓婏紝澧炲姞绮炬帓姝ラ杩涗竴姝ユ彁鍗囩浉鍏虫€с€?

鏈」鐩綋鍓嶉噰鐢?**娣峰悎鍙洖 + 绮炬帓锛圚ybrid + Rerank锛?* 绛栫暐锛?
- **绋犲瘑鍙洖锛圖ense Route锛?*锛氳绠?Query Embedding锛屽湪鍚戦噺搴撲腑杩涜 Cosine Similarity 妫€绱紝杩斿洖 Top-N 璇箟鍊欓€夈€?
- **绋€鐤忓彫鍥烇紙Sparse Route锛?*锛氫娇鐢?BM25 绠楁硶妫€绱㈠€掓帓绱㈠紩锛岃繑鍥?Top-N 鍏抽敭璇嶅€欓€夈€?
- **铻嶅悎锛團usion锛?*锛氫娇鐢?RRF (Reciprocal Rank Fusion) 绠楁硶灏嗕袱璺粨鏋滃悎骞舵帓搴忋€?
- **绮炬帓锛圧erank锛?*锛氬铻嶅悎鍚庣殑鍊欓€夐泦杩涜閲嶆帓搴忥紝鏀寔 None / Cross-Encoder / LLM Rerank 涓夌妯″紡銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熷疄鐜颁簡 Hybrid + Rerank 绛栫暐銆傛灦鏋勮璁′笂棰勭暀浜嗙瓥鐣ュ垏鎹㈣兘鍔涳紝濡傞渶浣跨敤绾瀵嗘垨绾█鐤忓彫鍥烇紝鍙€氳繃閰嶇疆鍒囨崲锛涜瀺鍚堢畻娉曞拰 Reranker 鍚屾牱鏀寔鏇挎崲銆?

#### 3.3.4 璇勪及妗嗘灦鎶借薄

璇勪及浣撶郴鐨勫彲鎻掓嫈鎬х‘淇濆洟闃熷彲浠ユ牴鎹笟鍔＄洰鏍囩伒娲婚€夋嫨鎴栫粍鍚堜笉鍚岀殑璐ㄩ噺搴﹂噺缁村害銆?

- **璁捐鎬濊矾**锛?
	- 瀹氫箟缁熶竴鐨?`Evaluator` 鎺ュ彛锛屾毚闇?`evaluate(query, retrieved_chunks, generated_answer, ground_truth) -> metrics` 鏂规硶銆?
	- 鍚勮瘎浼版鏋跺疄鐜拌鎺ュ彛锛岃緭鍑烘爣鍑嗗寲鐨勬寚鏍囧瓧鍏搞€?

- **鍙€夎瘎浼版鏋?*锛?

| 妗嗘灦 | 鐗圭偣 | 閫傜敤鍦烘櫙 |
|-----|------|---------|
| **Ragas** | RAG 涓撶敤銆佹寚鏍囦赴瀵岋紙Faithfulness, Answer Relevancy, Context Precision 绛夛級 | 鍏ㄩ潰璇勪及 RAG 璐ㄩ噺銆佸鏈姣?|
| **DeepEval** | LLM-as-Judge 妯″紡銆佹敮鎸佽嚜瀹氫箟璇勪及鏍囧噯 | 闇€瑕佷富瑙傝川閲忓垽鏂€佸鏉備笟鍔¤鍒?|
| **鑷畾涔夋寚鏍?* | Hit Rate, MRR, Latency P99 绛夊熀纭€宸ョ▼鎸囨爣 | 蹇€熷洖褰掓祴璇曘€佷笂绾垮墠 Sanity Check |

- **缁勫悎涓庢墿灞?*锛?
	- 璇勪及妯″潡璁捐涓?*缁勫悎妯″紡**锛屽彲鍚屾椂鎸傝浇澶氫釜 Evaluator锛岀敓鎴愮患鍚堟姤鍛娿€?
	- 閰嶇疆绀轰緥锛歚evaluation.backends: [ragas, custom_metrics]`锛岀郴缁熷苟琛屾墽琛屽苟姹囨€荤粨鏋溿€?

#### 3.3.5 閰嶇疆绠＄悊涓庡垏鎹㈡祦绋?

- **閰嶇疆鏂囦欢缁撴瀯绀轰緥** (`config/settings.yaml`)锛?
	```yaml
	llm:
	  provider: azure  # azure | openai | ollama | deepseek
	  model: gpt-4o
	  # provider-specific configs...
	
	embedding:
	  provider: openai
	  model: text-embedding-3-small
	
	vector_store:
	  backend: chroma  # chroma | qdrant | pinecone
	
	retrieval:
	  sparse_backend: bm25  # bm25 | elasticsearch
	  fusion_algorithm: rrf  # rrf | weighted_sum
	  rerank_backend: cross_encoder  # none | cross_encoder | llm
	
	evaluation:
	  backends: [ragas, custom_metrics]
	
	dashboard:
	  enabled: true
	  port: 8501
	  traces_dir: ./logs
	```

- **鍒囨崲娴佺▼**锛?

	1. 淇敼 `settings.yaml` 涓搴旂粍浠剁殑 `backend` / `provider` 瀛楁銆?
	2. 纭繚鏂板悗绔殑渚濊禆宸插畨瑁呫€佸嚟鎹凡閰嶇疆銆?
	3. 閲嶅惎鏈嶅姟锛屽伐鍘傚嚱鏁拌嚜鍔ㄥ姞杞芥柊瀹炵幇锛屾棤闇€淇敼涓氬姟浠ｇ爜銆?

### 3.4 鍙娴嬫€т笌鍙鍖栫鐞嗗钩鍙拌璁?(Observability & Visual Management Platform Design)

**鐩爣锛?* 閽堝 RAG 绯荤粺甯歌鐨?榛戠洅"闂锛岃璁″叏閾捐矾鍙娴嬬殑杩借釜浣撶郴涓庡畬鏁寸殑鍙鍖栫鐞嗗钩鍙般€傝鐩?**Ingestion锛堟憚鍙栭摼璺級** 涓?**Query锛堟煡璇㈤摼璺級** 涓ゆ潯瀹屾暣娴佹按绾跨殑杩借釜璁板綍锛屽悓鏃舵彁渚涙暟鎹祻瑙堛€佹枃妗ｇ鐞嗐€佺粍浠舵瑙堢瓑绠＄悊鍔熻兘锛屼娇鏁翠釜绯荤粺**閫忔槑鍙**銆?*鍙鐞?*涓?*鍙噺鍖?*銆?

#### 3.4.1 璁捐鐞嗗康

- **鍙岄摼璺叏瑕嗙洊杩借釜 (Dual-Pipeline Tracing)**锛?
    - **Ingestion Trace**锛氫互 `trace_id` 涓烘牳蹇冿紝璁板綍涓€娆℃憚鍙栦粠鏂囦欢鍔犺浇鍒板瓨鍌ㄥ畬鎴愮殑鍏ㄨ繃绋嬶紙load 鈫?split 鈫?transform 鈫?embed 鈫?upsert锛夛紝鍖呭惈鍚勯樁娈佃€楁椂銆佸鐞嗙殑 chunk 鏁伴噺銆佽烦杩?澶辫触璇︽儏銆?
    - **Query Trace**锛氫互 `trace_id` 涓烘牳蹇冿紝璁板綍涓€娆℃煡璇粠 Query 杈撳叆鍒?Response 杈撳嚭鐨勫叏杩囩▼锛坬uery_processing 鈫?dense 鈫?sparse 鈫?fusion 鈫?rerank锛夛紝鍖呭惈鍚勯樁娈靛€欓€夋暟閲忋€佸垎鏁板垎甯冧笌鑰楁椂銆?
- **閫忔槑鍙洖婧?(Transparent & Traceable)**锛氭瘡涓樁娈电殑涓棿鐘舵€侀兘琚褰曪紝寮€鍙戣€呭彲浠ユ竻鏅扮湅鍒?绯荤粺涓轰粈涔堝彫鍥炰簡杩欎簺鏂囨。"銆?Rerank 鍓嶅悗鎺掑悕濡備綍鍙樺寲"锛屼粠鑰岀簿鍑嗗畾浣嶉棶棰樸€?
- **浣庝镜鍏ユ€?(Low Intrusiveness)**锛氳拷韪€昏緫涓庝笟鍔￠€昏緫瑙ｈ€︼紝閫氳繃 `TraceContext` 鏄惧紡璋冪敤妯″紡娉ㄥ叆锛岄伩鍏嶆薄鏌撴牳蹇冧唬鐮併€?
- **杞婚噺鏈湴鍖?(Lightweight & Local)**锛氶噰鐢ㄧ粨鏋勫寲鏃ュ織 + 鏈湴 Dashboard 鐨勬柟妗堬紝闆跺閮ㄤ緷璧栵紝寮€绠卞嵆鐢ㄣ€?
- **鍔ㄦ€佺粍浠舵劅鐭?(Dynamic Component Awareness)**锛欴ashboard 鍩轰簬 Trace 涓殑 `method`/`provider`/`details` 瀛楁鍔ㄦ€佹覆鏌擄紝鏇存崲鍙彃鎷旂粍浠跺悗鑷姩閫傞厤灞曠ず鍐呭锛屾棤闇€淇敼 Dashboard 浠ｇ爜銆?


#### 3.4.2 杩借釜鏁版嵁缁撴瀯

绯荤粺瀹氫箟涓ょ被 Trace 璁板綍锛屽垎鍒鐩栨煡璇笌鎽勫彇涓ゆ潯閾捐矾锛?

**A. Query Trace锛堟煡璇㈣拷韪級**

姣忔鏌ヨ璇锋眰鐢熸垚鍞竴鐨?`trace_id`锛岃褰曚粠 Query 杈撳叆鍒?Response 杈撳嚭鐨勫叏杩囩▼锛?

**鍩虹淇℃伅**锛?
- `trace_id`锛氳姹傚敮涓€鏍囪瘑
- `trace_type`锛歚"query"`
- `timestamp`锛氳姹傛椂闂存埑
- `user_query`锛氱敤鎴峰師濮嬫煡璇?
- `collection`锛氭绱㈢殑鐭ヨ瘑搴撻泦鍚?

**鍚勯樁娈佃鎯?(Stages)**锛?

| 闃舵 | 璁板綍鍐呭 |
|-----|---------|
| **Query Processing** | 鍘熷 Query銆佹敼鍐欏悗 Query锛堣嫢鏈夛級銆佹彁鍙栫殑鍏抽敭璇嶃€乵ethod銆佽€楁椂 |
| **Dense Retrieval** | 杩斿洖鐨?Top-N 鍊欓€夊強鐩镐技搴﹀垎鏁般€乸rovider銆佽€楁椂 |
| **Sparse Retrieval** | 杩斿洖鐨?Top-N 鍊欓€夊強 BM25 鍒嗘暟銆乵ethod銆佽€楁椂 |
| **Fusion** | 铻嶅悎鍚庣殑缁熶竴鎺掑悕銆乤lgorithm銆佽€楁椂 |
| **Rerank** | 閲嶆帓鍚庣殑鏈€缁堟帓鍚嶅強鍒嗘暟銆乥ackend銆佹槸鍚﹁Е鍙?Fallback銆佽€楁椂 |

**姹囨€绘寚鏍?*锛?
- `total_latency`锛氱鍒扮鎬昏€楁椂
- `top_k_results`锛氭渶缁堣繑鍥炵殑 Top-K 鏂囨。 ID
- `error`锛氬紓甯镐俊鎭紙鑻ユ湁锛?

**璇勪及鎸囨爣 (Evaluation Metrics)**锛?
- `context_relevance`锛氬彫鍥炴枃妗ｄ笌 Query 鐨勭浉鍏虫€у垎鏁?
- `answer_faithfulness`锛氱敓鎴愮瓟妗堜笌鍙洖鏂囨。鐨勪竴鑷存€у垎鏁帮紙鑻ユ湁鐢熸垚鐜妭锛?

**B. Ingestion Trace锛堟憚鍙栬拷韪級**

姣忔鏂囨。鎽勫彇鐢熸垚鍞竴鐨?`trace_id`锛岃褰曚粠鏂囦欢鍔犺浇鍒板瓨鍌ㄥ畬鎴愮殑鍏ㄨ繃绋嬶細

**鍩虹淇℃伅**锛?
- `trace_id`锛氭憚鍙栧敮涓€鏍囪瘑
- `trace_type`锛歚"ingestion"`
- `timestamp`锛氭憚鍙栧紑濮嬫椂闂?
- `source_path`锛氭簮鏂囦欢璺緞
- `collection`锛氱洰鏍囬泦鍚堝悕绉?

**鍚勯樁娈佃鎯?(Stages)**锛?

| 闃舵 | 璁板綍鍐呭 |
|-----|---------|
| **Load** | 鏂囦欢澶у皬銆佽В鏋愬櫒锛坢ethod: markitdown锛夈€佹彁鍙栫殑鍥剧墖鏁般€佽€楁椂 |
| **Split** | splitter 绫诲瀷锛坢ethod锛夈€佷骇鍑?chunk 鏁般€佸钩鍧?chunk 闀垮害銆佽€楁椂 |
| **Transform** | 鍚?transform 鍚嶇О涓庡鐞嗚鎯咃紙refined/enriched/captioned 鏁伴噺锛夈€丩LM provider銆佽€楁椂 |
| **Embed** | embedding provider銆乥atch 鏁般€佸悜閲忕淮搴︺€乨ense + sparse 缂栫爜鑰楁椂 |
| **Upsert** | 瀛樺偍鍚庣锛坢ethod: chroma锛夈€乽psert 鏁伴噺銆丅M25 绱㈠紩鏇存柊銆佸浘鐗囧瓨鍌ㄣ€佽€楁椂 |

**姹囨€绘寚鏍?*锛?
- `total_latency`锛氱鍒扮鎬昏€楁椂
- `total_chunks`锛氭渶缁堝瓨鍌ㄧ殑 chunk 鏁伴噺
- `total_images`锛氬鐞嗙殑鍥剧墖鏁伴噺
- `skipped`锛氳烦杩囩殑鏂囦欢/chunk 鏁帮紙宸插瓨鍦ㄣ€佹湭鍙樻洿绛夛級
- `error`锛氬紓甯镐俊鎭紙鑻ユ湁锛?


#### 3.4.3 鎶€鏈柟妗堬細缁撴瀯鍖栨棩蹇?+ 鏈湴 Web Dashboard

鏈」鐩噰鐢?**"缁撴瀯鍖栨棩蹇?+ 鏈湴 Web Dashboard"** 浣滀负鍙娴嬫€х殑瀹炵幇鏂规銆?

**閫夊瀷鐞嗙敱**锛?
- **闆跺閮ㄤ緷璧?*锛氫笉渚濊禆 LangSmith銆丩angFuse 绛夌涓夋柟骞冲彴锛屾棤闇€缃戠粶杩炴帴涓庤处鍙锋敞鍐岋紝瀹屽叏鏈湴鍖栬繍琛屻€?
- **杞婚噺鏄撻儴缃?*锛氫粎闇€ Python 鏍囧噯搴?+ 涓€涓交閲?Web 妗嗘灦锛堝 Streamlit锛夛紝`pip install` 鍗冲彲浣跨敤锛屾棤闇€ Docker 鎴栨暟鎹簱鏈嶅姟銆?
- **瀛︿範鎴愭湰浣?*锛氱粨鏋勫寲鏃ュ織鏄€氱敤鎶€鑳斤紝璋冭瘯鏃跺彲鐩存帴鐢?`jq`銆乣grep` 绛夊懡浠よ宸ュ叿鏌ヨ锛汥ashboard 浠ｇ爜绠€鍗曠洿瑙傦紝渚夸簬鐞嗚В涓庝簩娆″紑鍙戙€?
- **濂戝悎椤圭洰瀹氫綅**锛氭湰椤圭洰闈㈠悜鏈湴 MCP Server 鍦烘櫙锛屽崟鐢ㄦ埛銆佸崟鏈鸿繍琛岋紝鏃犻渶鍒嗗竷寮忚拷韪垨澶氱鎴烽殧绂荤瓑浼佷笟绾ц兘鍔涖€?

**瀹炵幇鏋舵瀯**锛?

```
RAG Pipeline
    鈹?
    鈻?
Trace Collector (瑁呴グ鍣?鍥炶皟)
    鈹?
    鈻?
JSON Lines 鏃ュ織鏂囦欢 (logs/traces.jsonl)
    鈹?
    鈻?
鏈湴 Web Dashboard (Streamlit)
    鈹?
    鈻?
鎸?trace_id 鏌ョ湅鍚勯樁娈佃鎯呬笌鎬ц兘鎸囨爣
```

**鏍稿績缁勪欢**锛?
- **缁撴瀯鍖栨棩蹇楀眰**锛氬熀浜?Python `logging` + JSON Formatter锛屽皢姣忔璇锋眰鐨?Trace 鏁版嵁浠?JSON Lines 鏍煎紡杩藉姞鍐欏叆鏈湴鏂囦欢銆傛瘡琛屼竴鏉″畬鏁寸殑璇锋眰璁板綍锛屽寘鍚?`trace_id`銆佸悇闃舵璇︽儏涓庤€楁椂銆?
- **鏈湴 Web Dashboard**锛氬熀浜?Streamlit 鏋勫缓鐨勮交閲忕骇 Web UI锛岃鍙栨棩蹇楁枃浠跺苟鎻愪緵浜や簰寮忓彲瑙嗗寲銆傛牳蹇冨姛鑳芥槸鎸?`trace_id` 妫€绱㈠苟灞曠ず鍗曟璇锋眰鐨勫畬鏁磋拷韪摼璺€?

#### 3.4.4 杩借釜鏈哄埗瀹炵幇

涓虹‘淇濆悇 RAG 闃舵锛堝彲鏇挎崲銆佸彲鑷畾涔夛級閮借兘杈撳嚭缁熶竴鏍煎紡鐨勮拷韪棩蹇楋紝绯荤粺閲囩敤 **TraceContext锛堣拷韪笂涓嬫枃锛?* 浣滀负鏍稿績鏈哄埗銆?

**宸ヤ綔鍘熺悊**锛?

1. **璇锋眰寮€濮?*锛歅ipeline 鍏ュ彛鍒涘缓涓€涓?`TraceContext` 瀹炰緥锛岀敓鎴愬敮涓€ `trace_id`锛岃褰曡姹傚熀纭€淇℃伅锛圦uery銆丆ollection 绛夛級銆?

2. **闃舵璁板綍**锛歚TraceContext` 鎻愪緵 `record_stage()` 鏂规硶锛屽悇闃舵鎵ц瀹屾瘯鍚庤皟鐢ㄨ鏂规硶锛屼紶鍏ラ樁娈靛悕绉般€佽€楁椂銆佽緭鍏ヨ緭鍑虹瓑鏁版嵁銆?

3. **璇锋眰缁撴潫**锛氳皟鐢?`trace.finish()`锛宍TraceContext` 灏嗘敹闆嗙殑瀹屾暣鏁版嵁搴忓垪鍖栦负 JSON锛岃拷鍔犲啓鍏ユ棩蹇楁枃浠躲€?

**涓庡彲鎻掓嫈缁勪欢鐨勯厤鍚?*锛?
- 鍚勯樁娈电粍浠讹紙Retriever銆丷eranker 绛夛級鐨勬帴鍙ｇ害瀹氫腑鍖呭惈 `TraceContext` 鍙傛暟銆?
- 缁勪欢瀹炵幇鑰呭湪鎵ц鏍稿績閫昏緫鍚庯紝璋冪敤 `trace.record_stage()` 璁板綍鏈樁娈电殑鍏抽敭淇℃伅銆?
- 杩欐槸**鏄惧紡璋冪敤**妯″紡锛氫笉寮哄埗銆佷笉浼氬洜鏈皟鐢ㄨ€屾姤閿欙紝浣嗕緷璧栧紑鍙戣€呬富鍔ㄨ褰曘€傚ソ澶勬槸浠ｇ爜閫忔槑锛屽紑鍙戣€呮竻妤氱煡閬撳摢浜涙暟鎹璁板綍锛涗唬浠锋槸闇€瑕佸紑鍙戣€呰嚜瑙夐伒瀹堢害瀹氥€?

**闃舵鍒掑垎鍘熷垯**锛?
- **Stage 鏄浐瀹氱殑閫氱敤澶х被**锛歚retrieval`锛堟绱級銆乣rerank`锛堥噸鎺掞級銆乣generation`锛堢敓鎴愶級绛夛紝涓嶉殢鍏蜂綋瀹炵幇鏂规鍙樺寲銆?
- **鍏蜂綋瀹炵幇鏄樁娈靛唴閮ㄧ殑缁嗚妭**锛氬湪 `record_stage()` 涓€氳繃 `method` 瀛楁璁板綍閲囩敤鐨勫叿浣撴柟娉曪紙濡?`bm25`銆乣hybrid`锛夛紝閫氳繃 `details` 瀛楁璁板綍鏂规硶鐩稿叧鐨勭粏鑺傛暟鎹€?
- 杩欐牱鏃犺搴曞眰鏂规鎬庝箞鏇挎崲锛岄樁娈电粨鏋勪繚鎸佺ǔ瀹氾紝Dashboard 灞曠ず閫昏緫鏃犻渶璋冩暣銆?

#### 3.4.5 Dashboard 鍔熻兘璁捐锛堝叚椤甸潰鏋舵瀯锛?

Dashboard 鍩轰簬 Streamlit 鏋勫缓澶氶〉闈㈠簲鐢紙`st.navigation`锛夛紝鎻愪緵鍏ぇ鍔熻兘椤甸潰锛?

**椤甸潰 1锛氱郴缁熸€昏 (Overview)**
- **缁勪欢閰嶇疆鍗＄墖**锛氳鍙?`Settings`锛屽睍绀哄綋鍓嶅彲鎻掓嫈缁勪欢鐨勯厤缃姸鎬侊細
    - LLM锛歱rovider + model锛堝 `azure / gpt-4o`锛?
    - Embedding锛歱rovider + model + 缁村害
    - Splitter锛氱被鍨?+ chunk_size + overlap
    - Reranker锛歜ackend + model锛堟垨 None锛?
    - Evaluator锛氬凡鍚敤鐨?backends 鍒楄〃
- **鏁版嵁璧勪骇缁熻**锛氳皟鐢?`DocumentManager.get_collection_stats()` 灞曠ず鍚勯泦鍚堢殑鏂囨。鏁般€乧hunk 鏁般€佸浘鐗囨暟銆?
- **绯荤粺鍋ュ悍鎸囨爣**锛氭渶杩戜竴娆?Ingestion/Query trace 鐨勬椂闂翠笌鑰楁椂銆?

**椤甸潰 2锛氭暟鎹祻瑙堝櫒 (Data Browser)**
- **鏂囨。鍒楄〃瑙嗗浘**锛氬睍绀哄凡鎽勫叆鐨勬枃妗ｏ紙source_path銆侀泦鍚堛€乧hunk 鏁般€佹憚鍏ユ椂闂达級锛屾敮鎸佹寜闆嗗悎绛涢€変笌鍏抽敭璇嶆悳绱€?
- **Chunk 璇︽儏瑙嗗浘**锛氱偣鍑绘枃妗ｅ睍寮€鍏舵墍鏈?chunk锛屾瘡涓?chunk 鏄剧ず锛?
    - 鍘熸枃鍐呭锛堝彲鎶樺彔闀挎枃鏈級
    - Metadata 鍚勫瓧娈碉紙title銆乻ummary銆乼ags銆乸age銆乮mage_refs 绛夛級
    - 鍏宠仈鍥剧墖棰勮锛堜粠 ImageStorage 璇诲彇骞跺睍绀虹缉鐣ュ浘锛?
- **鏁版嵁鏉ユ簮**锛氶€氳繃 `ChromaStore.get_all()` 鎴?`get_by_metadata()` 璇诲彇 chunk 鏁版嵁銆?

**椤甸潰 3锛欼ngestion 绠＄悊 (Ingestion Manager)**
- **鏂囦欢閫夋嫨涓庢憚鍙栬Е鍙?*锛?
    - 鏂囦欢涓婁紶缁勪欢锛坄st.file_uploader`锛夋垨鐩綍璺緞杈撳叆
    - 閫夋嫨鐩爣闆嗗悎锛堜笅鎷夐€夋嫨鎴栨柊寤猴級
    - 鐐瑰嚮"寮€濮嬫憚鍙?鎸夐挳瑙﹀彂 `IngestionPipeline.run()`
    - 鍒╃敤 `on_progress` 鍥炶皟椹卞姩 Streamlit 杩涘害鏉★紙`st.progress`锛夛紝瀹炴椂鏄剧ず褰撳墠闃舵涓庡鐞嗚繘搴?
- **鏂囨。鍒犻櫎**锛?
    - 鍦ㄦ枃妗ｅ垪琛ㄤ腑鎻愪緵"鍒犻櫎"鎸夐挳
    - 璋冪敤 `DocumentManager.delete_document()` 鍗忚皟璺ㄥ瓨鍌ㄥ垹闄?
    - 鍒犻櫎瀹屾垚鍚庡埛鏂板垪琛?
- **娉ㄦ剰**锛歅ipeline 鎵ц涓哄悓姝ラ樆濉炴搷浣滐紝Streamlit 鐨?rerun 鏈哄埗澶╃劧鏀寔锛堣繘搴︽潯鍦ㄥ悓涓€ request 涓洿鏂帮級銆?

**椤甸潰 4锛欼ngestion 杩借釜 (Ingestion Traces)**
- **鎽勫彇鍘嗗彶鍒楄〃**锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "ingestion"` 鐨勫巻鍙茶褰曪紝鏄剧ず鏂囦欢鍚嶃€侀泦鍚堛€佹€昏€楁椂銆佺姸鎬侊紙鎴愬姛/澶辫触锛夈€?
- **鍗曟鎽勫彇璇︽儏**锛?
    - **闃舵鑰楁椂鐎戝竷鍥?*锛氭í鍚戞潯褰㈠浘灞曠ず load/split/transform/embed/upsert 鍚勯樁娈垫椂闂村垎甯冦€?
    - **澶勭悊缁熻**锛歝hunk 鏁般€佸浘鐗囨暟銆佽烦杩囨暟銆佸け璐ユ暟銆?
    - **鍚勯樁娈佃鎯呭睍寮€**锛氱偣鍑绘煡鐪?method/provider銆佽緭鍏ヨ緭鍑烘牱鏈€?

**椤甸潰 5锛歈uery 杩借釜 (Query Traces)**
- **鏌ヨ鍘嗗彶鍒楄〃**锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "query"` 鐨勫巻鍙茶褰曪紝鏀寔鎸?Query 鍏抽敭璇嶇瓫閫夈€?
- **鍗曟鏌ヨ璇︽儏**锛?
    - **鑰楁椂鐎戝竷鍥?*锛氬睍绀?query_processing/dense/sparse/fusion/rerank 鍚勯樁娈垫椂闂村垎甯冦€?
    - **Dense vs Sparse 瀵规瘮**锛氬苟鍒楀睍绀轰袱璺彫鍥炵粨鏋滅殑 Top-N 鏂囨。 ID 涓庡垎鏁般€?
    - **Rerank 鍓嶅悗瀵规瘮**锛氬睍绀鸿瀺鍚堟帓鍚嶄笌绮炬帓鍚庢帓鍚嶇殑鍙樺寲锛堟帓鍚嶈穬鍗?涓嬮檷鏍囪锛夈€?
    - **鏈€缁堢粨鏋滆〃**锛氬睍绀?Top-K 鍊欓€夋枃妗ｇ殑鏍囬銆佸垎鏁般€佹潵婧愩€?

**椤甸潰 6锛氳瘎浼伴潰鏉?(Evaluation Panel)**
- **璇勪及杩愯**锛氶€夋嫨璇勪及鍚庣锛圧agas / Custom / All锛変笌 golden test set锛岀偣鍑昏繍琛屻€?
- **鎸囨爣灞曠ず**锛氫互琛ㄦ牸鍜屽浘琛ㄥ睍绀?hit_rate銆乵rr銆乫aithfulness 绛夋寚鏍囥€?
- **鍘嗗彶瓒嬪娍**锛氬姣斾笉鍚屾椂闂寸殑璇勪及缁撴灉锛岃瀵熺瓥鐣ヨ皟鏁寸殑鏁堟灉銆?
- **娉ㄦ剰**锛氳瘎浼伴潰鏉垮湪 Phase H 瀹炵幇锛孭hase G 瀹屾垚鍚庤椤甸潰鏄剧ず"璇勪及妯″潡灏氭湭鍚敤"鐨勫崰浣嶆彁绀恒€?

**Dashboard 鎶€鏈灦鏋?*锛?

```
src/observability/dashboard/
鈹溾攢鈹€ app.py                    # Streamlit 鍏ュ彛锛岄〉闈㈠鑸敞鍐?
鈹溾攢鈹€ pages/
鈹?  鈹溾攢鈹€ overview.py           # 椤甸潰 1锛氱郴缁熸€昏
鈹?  鈹溾攢鈹€ data_browser.py       # 椤甸潰 2锛氭暟鎹祻瑙堝櫒
鈹?  鈹溾攢鈹€ ingestion_manager.py  # 椤甸潰 3锛欼ngestion 绠＄悊
鈹?  鈹溾攢鈹€ ingestion_traces.py   # 椤甸潰 4锛欼ngestion 杩借釜
鈹?  鈹溾攢鈹€ query_traces.py       # 椤甸潰 5锛歈uery 杩借釜
鈹?  鈹斺攢鈹€ evaluation_panel.py   # 椤甸潰 6锛氳瘎浼伴潰鏉?
鈹斺攢鈹€ services/
    鈹溾攢鈹€ trace_service.py      # Trace 鏁版嵁璇诲彇鏈嶅姟锛堣В鏋?traces.jsonl锛?
    鈹溾攢鈹€ data_service.py       # 鏁版嵁娴忚鏈嶅姟锛堝皝瑁?ChromaStore/ImageStorage 璇诲彇锛?
    鈹斺攢鈹€ config_service.py     # 閰嶇疆璇诲彇鏈嶅姟锛堝皝瑁?Settings 璇诲彇涓庡睍绀猴級
```

**Dashboard 涓?Trace 鐨勬暟鎹叧绯?*锛?
- Dashboard 椤甸潰 4/5 璇诲彇 `logs/traces.jsonl`锛堥€氳繃 `TraceService`锛夛紝鎸?`trace_type` 鍒嗙被灞曠ず銆?
- Dashboard 椤甸潰 1/2/3 鐩存帴璇诲彇瀛樺偍灞傦紙閫氳繃 `DataService` 灏佽 ChromaStore/ImageStorage/FileIntegrity锛夛紝涓嶄緷璧?Trace銆?
- 鎵€鏈夐〉闈㈠熀浜?Trace 涓?`method`/`provider` 瀛楁鍔ㄦ€佹覆鏌撴爣绛撅紝鏇存崲缁勪欢鍚庤嚜鍔ㄩ€傞厤銆?


#### 3.4.6 閰嶇疆绀轰緥

```yaml
observability:
  enabled: true
  
  # 鏃ュ織閰嶇疆
  logging:
    log_file: logs/traces.jsonl  # JSON Lines 鏍煎紡鏃ュ織鏂囦欢
    log_level: INFO  # DEBUG | INFO | WARNING
  
  # 杩借釜绮掑害鎺у埗
  detail_level: standard  # minimal | standard | verbose

# Dashboard 绠＄悊骞冲彴閰嶇疆
dashboard:
  enabled: true
  port: 8501                     # Streamlit 鏈嶅姟绔彛
  traces_dir: ./logs             # Trace 鏃ュ織鏂囦欢鐩綍
  auto_refresh: true             # 鏄惁鑷姩鍒锋柊锛堣疆璇㈡柊 trace锛?
  refresh_interval: 5            # 鑷姩鍒锋柊闂撮殧锛堢锛?
```


### 3.5 澶氭ā鎬佸浘鐗囧鐞嗚璁?(Multimodal Image Processing Design)

**鐩爣锛?* 璁捐涓€濂楀畬鏁寸殑鍥剧墖澶勭悊鏂规锛屼娇 RAG 绯荤粺鑳藉鐞嗚В銆佺储寮曞苟妫€绱㈡枃妗ｄ腑鐨勫浘鐗囧唴瀹癸紝瀹炵幇"鐢ㄨ嚜鐒惰瑷€鎼滅储鍥剧墖"鐨勮兘鍔涳紝鍚屾椂淇濇寔鏋舵瀯鐨勭畝娲佹€т笌鍙墿灞曟€с€?

#### 3.5.1 璁捐鐞嗗康涓庣瓥鐣ラ€夊瀷

澶氭ā鎬?RAG 鐨勬牳蹇冩寫鎴樺湪浜庯細**濡備綍璁╃函鏂囨湰鐨勬绱㈢郴缁?鐪嬫噦"鍥剧墖**銆備笟鐣屼富瑕佹湁涓ょ鎶€鏈矾绾匡細

| 绛栫暐 | 鏍稿績鎬濊矾 | 浼樺娍 | 鍔ｅ娍 |
|-----|---------|------|------|
| **Image-to-Text (鍥捐浆鏂?** | 鍒╃敤 Vision LLM 灏嗗浘鐗囪浆鍖栦负鏂囨湰鎻忚堪锛屽鐢ㄧ函鏂囨湰 RAG 閾捐矾 | 鏋舵瀯缁熶竴銆佸疄鐜扮畝鍗曘€佹垚鏈彲鎺?| 鎻忚堪璐ㄩ噺渚濊禆 LLM 鑳藉姏锛屽彲鑳戒涪澶辫瑙夌粏鑺?|
| **Multi-Embedding (澶氭ā鎬佸悜閲?** | 浣跨敤 CLIP 绛夋ā鍨嬪皢鍥炬枃缁熶竴鏄犲皠鍒板悓涓€鍚戦噺绌洪棿 | 淇濈暀鍘熷瑙嗚鐗瑰緛锛屾敮鎸佸浘鎼滃浘 | 闇€寮曞叆棰濆鍚戦噺搴擄紝鏋舵瀯澶嶆潅搴﹂珮 |

**鏈」鐩€夊瀷锛欼mage-to-Text锛堝浘杞枃锛夌瓥鐣?*

閫夊瀷鐞嗙敱锛?
- **鏋舵瀯缁熶竴**锛氭棤闇€寮曞叆 CLIP 绛夊妯℃€?Embedding 妯″瀷锛屾棤闇€缁存姢鐙珛鐨勫浘鍍忓悜閲忓簱锛屽畬鍏ㄥ鐢ㄧ幇鏈夌殑鏂囨湰 RAG 閾捐矾锛圛ngestion 鈫?Hybrid Search 鈫?Rerank锛夈€?
- **璇箟瀵归綈**锛氶€氳繃 LLM 灏嗗浘鐗囩殑瑙嗚淇℃伅杞寲涓鸿嚜鐒惰瑷€鎻忚堪锛屽ぉ鐒朵笌鐢ㄦ埛鐨勬枃鏈煡璇㈠湪鍚屼竴璇箟绌洪棿锛屾绱㈡晥鏋滃彲棰勬湡銆?
- **鎴愭湰鍙帶**锛氫粎鍦ㄦ暟鎹憚鍙栭樁娈典竴娆℃€ц皟鐢?Vision LLM锛屾绱㈤樁娈垫棤棰濆鎴愭湰銆?
- **娓愯繘澧炲己**锛氭湭鏉ュ闇€鏀寔"鍥炬悳鍥?绛夐珮绾ц兘鍔涳紝鍙湪姝ゅ熀纭€涓婂彔鍔?CLIP Embedding锛屾棤闇€閲嶆瀯鏍稿績閾捐矾銆?

#### 3.5.2 鍥剧墖澶勭悊鍏ㄦ祦绋嬭璁?

鍥剧墖澶勭悊璐┛ Ingestion Pipeline 鐨勫涓樁娈碉紝鏁翠綋娴佺▼濡備笅锛?

```
鍘熷鏂囨。 (PDF/PPT/Markdown)
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Loader 闃舵锛氬浘鐗囨彁鍙栦笌寮曠敤鏀堕泦                           鈹?
鈹? - 瑙ｆ瀽鏂囨。锛岃瘑鍒苟鎻愬彇宓屽叆鐨勫浘鐗囪祫婧?                       鈹?
鈹? - 涓烘瘡寮犲浘鐗囩敓鎴愬敮涓€鏍囪瘑 (image_id)                       鈹?
鈹? - 鍦ㄦ枃妗ｆ枃鏈腑鎻掑叆鍥剧墖鍗犱綅绗?寮曠敤鏍囪                       鈹?
鈹? - 杈撳嚭锛欴ocument (text + metadata.images[])             鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Splitter 闃舵锛氫繚鎸佸浘鏂囧叧鑱?                              鈹?
鈹? - 鍒囧垎鏃朵繚鐣欏浘鐗囧紩鐢ㄦ爣璁板湪瀵瑰簲 Chunk 涓?                    鈹?
鈹? - 纭繚鍥剧墖涓庡叾涓婁笅鏂囨钀戒繚鎸佸叧鑱?                           鈹?
鈹? - 杈撳嚭锛欳hunks (鍚勮嚜鎼哄甫鍏宠仈鐨?image_refs)                鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Transform 闃舵锛氬浘鐗囩悊瑙ｄ笌鎻忚堪鐢熸垚                         鈹?
鈹? - 璋冪敤 Vision LLM 瀵规瘡寮犲浘鐗囩敓鎴愮粨鏋勫寲鎻忚堪                  鈹?
鈹? - 灏嗘弿杩版枃鏈敞鍏ュ埌鍏宠仈 Chunk 鐨勬鏂囨垨 Metadata 涓?          鈹?
鈹? - 杈撳嚭锛欵nriched Chunks (鍚浘鐗囪涔変俊鎭?                  鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Storage 闃舵锛氬弻杞ㄥ瓨鍌?                                   鈹?
鈹? - 鍚戦噺搴擄細瀛樺偍澧炲己鍚庣殑 Chunk (鍚浘鐗囨弿杩? 鐢ㄤ簬妫€绱?          鈹?
鈹? - 鏂囦欢绯荤粺/Blob锛氬瓨鍌ㄥ師濮嬪浘鐗囨枃浠剁敤浜庤繑鍥炲睍绀?               鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

#### 3.5.3 鍚勯樁娈垫妧鏈鐐?

**1. Loader 闃舵锛氬浘鐗囨彁鍙栦笌寮曠敤鏀堕泦**

- **鎻愬彇绛栫暐**锛?
  - 瑙ｆ瀽鏂囨。鏃惰瘑鍒祵鍏ョ殑鍥剧墖璧勬簮锛圥DF 涓殑 XObject銆丳PT 涓殑濯掍綋鏂囦欢銆丮arkdown 涓殑 `![]()` 寮曠敤锛夈€?
  - 涓烘瘡寮犲浘鐗囩敓鎴愬叏灞€鍞竴鐨?`image_id`锛堝缓璁牸寮忥細`{doc_hash}_{page}_{seq}`锛夈€?
  - 灏嗗浘鐗囦簩杩涘埗鏁版嵁鎻愬彇骞舵殏瀛橈紝璁板綍鍏跺湪鍘熸枃妗ｄ腑鐨勪綅缃俊鎭€?

- **寮曠敤鏍囪**锛?
  - 鍦ㄨ浆鎹㈠悗鐨?Markdown 鏂囨湰涓紝浜庡浘鐗囧師濮嬩綅缃彃鍏ュ崰浣嶇锛堝 `[IMAGE: {image_id}]`锛夈€?
  - 鍦?Document 鐨?Metadata 涓淮鎶?`images` 鍒楄〃锛岃褰曟瘡寮犲浘鐗囩殑 `image_id`銆佸師濮嬭矾寰勩€侀〉鐮併€佸昂瀵哥瓑鍩虹淇℃伅銆?

- **瀛樺偍鍘熷鍥剧墖**锛?
  - 灏嗘彁鍙栫殑鍥剧墖淇濆瓨鑷虫湰鍦版枃浠剁郴缁熺殑绾﹀畾鐩綍锛堝 `data/images/{collection}/{image_id}.png`锛夈€?
  - 浠呬繚瀛橀渶瑕佺殑鍥剧墖鏍煎紡锛堟帹鑽愮粺涓€杞崲涓?PNG/JPEG锛夛紝鎺у埗瀛樺偍浣撶Н銆?

**2. Splitter 闃舵锛氫繚鎸佸浘鏂囧叧鑱?*

- **鍏宠仈淇濇寔鍘熷垯**锛?
  - 鍥剧墖寮曠敤鏍囪搴斾笌鍏惰鏄庢€ф枃瀛楋紙Caption銆佸墠鍚庢钀斤級灏介噺淇濇寔鍦ㄥ悓涓€ Chunk 涓€?
  - 鑻ュ浘鐗囧嚭鐜板湪绔犺妭寮€澶存垨缁撳熬锛屽垏鍒嗘椂搴斿皢鍏跺綊鍏ヨ涔変笂鏈€鐩稿叧鐨?Chunk銆?

- **Chunk Metadata 鎵╁睍**锛?
  - 姣忎釜 Chunk 鐨?Metadata 涓鍔?`image_refs: List[image_id]` 瀛楁锛岃褰曡 Chunk 鍏宠仈鐨勫浘鐗囧垪琛ㄣ€?
  - 姝ゅ瓧娈电敤浜庡悗缁?Transform 闃舵瀹氫綅闇€瑕佸鐞嗙殑鍥剧墖锛屼互鍙婃绱㈠懡涓悗瀹氫綅闇€瑕佽繑鍥炵殑鍥剧墖銆?

**3. Transform 闃舵锛氬浘鐗囩悊瑙ｄ笌鎻忚堪鐢熸垚**

杩欐槸澶氭ā鎬佸鐞嗙殑鏍稿績鐜妭锛岃礋璐ｅ皢瑙嗚淇℃伅杞寲涓哄彲妫€绱㈢殑鏂囨湰璇箟銆?

- **Vision LLM 閫夊瀷**锛?

| 妯″瀷 | 鎻愪緵鍟?| 鐗圭偣 | 閫傜敤鍦烘櫙 | 鎺ㄨ崘鎸囨暟 |
|-----|--------|------|---------|---------|
| **GPT-4o** | OpenAI / Azure | 鐞嗚В鑳藉姏寮猴紝鏀寔澶嶆潅鍥捐〃瑙ｈ锛岃嫳鏂囨枃妗ｈ〃鐜颁紭寮?| 楂樿川閲忛渶姹傘€佸鏉備笟鍔℃枃妗ｃ€佸浗闄呭寲鍦烘櫙 | 猸愨瓙猸愨瓙猸?|
| **Qwen-VL-Max** | 闃块噷浜?(DashScope) | 涓枃鐞嗚В鑳藉姏鍑鸿壊锛屾€т环姣旈珮锛屽涓枃鍥捐〃/鏂囨。鏀寔濂?| 涓枃鏂囨。銆佸浗鍐呴儴缃层€佹垚鏈晱鎰熷満鏅?| 猸愨瓙猸愨瓙猸?|
| **Qwen-VL-Plus** | 闃块噷浜?(DashScope) | 閫熷害鏇村揩锛屾垚鏈洿浣庯紝閫傚悎澶ф壒閲忓鐞?| 澶ф壒閲忎腑鏂囨枃妗ｃ€佸揩閫熻凯浠ｅ満鏅?| 猸愨瓙猸愨瓙 |
| **Claude 3.5 Sonnet** | Anthropic | 澶氭ā鎬佸師鐢熸敮鎸侊紝闀夸笂涓嬫枃 | 闇€瑕佺粨鍚堝ぇ娈垫枃瀛楃悊瑙ｅ浘鐗?| 猸愨瓙猸愨瓙 |
| **Gemini Pro Vision** | Google | 鎴愭湰杈冧綆锛岄€熷害杈冨揩 | 澶ф壒閲忓鐞嗐€佹垚鏈晱鎰熷満鏅?| 猸愨瓙猸?|
| **GLM-4V** | 鏅鸿氨 AI (ZhipuAI) | 鍥藉唴鑰佺墝锛岀ǔ瀹氭€уソ锛屼腑鏂囨敮鎸佷匠 | 鍥藉唴閮ㄧ讲澶囬€夈€佷紒涓氱骇搴旂敤 | 猸愨瓙猸愨瓙 |

**鍙屾ā鍨嬮€夊瀷绛栫暐锛堟帹鑽愶級**锛?

鏈」鐩噰鐢?*鍥藉唴 + 鍥藉鍙屾ā鍨?*鏂规锛岄€氳繃閰嶇疆鍒囨崲锛屽吋椤句笉鍚岄儴缃茬幆澧冨拰鏂囨。绫诲瀷锛?

| 閮ㄧ讲鐜 | 涓婚€夋ā鍨?| 澶囬€夋ā鍨?| 璇存槑 |
|---------|---------|---------|------|
| **鍥介檯鍖?/ Azure 鐜** | GPT-4o (Azure) | Qwen-VL-Max | 鑻辨枃鏂囨。浼樺厛鐢?GPT-4o锛屼腑鏂囨枃妗ｅ彲鍒囨崲 Qwen-VL |
| **鍥藉唴閮ㄧ讲 / 绾腑鏂囧満鏅?* | Qwen-VL-Max | GPT-4o | 涓枃鍥捐〃鐞嗚В鐢?Qwen-VL锛岀壒娈婇渶姹傚彲鍒囨崲 GPT-4o |
| **鎴愭湰鏁忔劅 / 澶ф壒閲?* | Qwen-VL-Plus | Gemini Pro Vision | 鐗虹壊閮ㄥ垎璐ㄩ噺鎹㈠彇閫熷害鍜屾垚鏈?|

**閫夊瀷鐞嗙敱**锛?

1. **GPT-4o (鍥藉棣栭€?**锛?
   - 瑙嗚鐞嗚В鑳藉姏涓氱晫棰嗗厛锛屽鏉傚浘琛ㄨВ璇诲噯纭巼楂?
   - Azure 閮ㄧ讲鍙弧瓒充紒涓氬悎瑙勮姹?
   - 鑻辨枃鎶€鏈枃妗ｇ悊瑙ｆ晥鏋滄渶浣?

2. **Qwen-VL-Max (鍥藉唴棣栭€?**锛?
   - 涓枃鍦烘櫙涓嬭〃鐜颁笌 GPT-4o 鎺ヨ繎锛岄儴鍒嗕腑鏂囧浘琛ㄤ换鍔＄敋鑷虫洿浼?
   - 閫氳繃闃块噷浜?DashScope API 璋冪敤锛屽浗鍐呰闂ǔ瀹氥€佸欢杩熶綆
   - 浠锋牸绾︿负 GPT-4o 鐨?1/3 ~ 1/5锛屾€т环姣旀瀬楂?
   - 鍘熺敓鏀寔涓枃 OCR锛屽涓枃鎴浘銆佽〃鏍艰瘑鍒洿鍑嗙‘

- **鎻忚堪鐢熸垚绛栫暐**锛?
  - **缁撴瀯鍖?Prompt**锛氳璁′笓鐢ㄧ殑鍥剧墖鐞嗚В Prompt锛屽紩瀵?LLM 杈撳嚭缁撴瀯鍖栨弿杩帮紝鑰岄潪鑷敱鍙戞尌銆?
  - **涓婁笅鏂囨劅鐭?*锛氬皢鍥剧墖鐨勫墠鍚庢枃鏈钀戒竴骞朵紶鍏?Vision LLM锛屽府鍔╁叾鐞嗚В鍥剧墖鍦ㄦ枃妗ｄ腑鐨勮澧冧笌浣滅敤銆?
  - **鍒嗙被鍨嬪鐞?*锛氶拡瀵逛笉鍚岀被鍨嬬殑鍥剧墖閲囩敤宸紓鍖栫殑鐞嗚В绛栫暐锛?

| 鍥剧墖绫诲瀷 | 鐞嗚В閲嶇偣 | Prompt 寮曞鏂瑰悜 |
|---------|---------|----------------|
| **娴佺▼鍥?鏋舵瀯鍥?* | 鑺傜偣銆佽繛鎺ュ叧绯汇€佹祦绋嬮€昏緫 | "鎻忚堪杩欏紶鍥剧殑缁撴瀯鍜屾祦绋嬫楠? |
| **鏁版嵁鍥捐〃** | 鏁版嵁瓒嬪娍銆佸叧閿暟鍊笺€佸姣斿叧绯?| "鎻愬彇鍥捐〃涓殑鍏抽敭鏁版嵁鍜岀粨璁? |
| **鎴浘/UI** | 鐣岄潰鍏冪礌銆佹搷浣滄寚寮曘€佺姸鎬佷俊鎭?| "鎻忚堪鎴浘涓殑鐣岄潰鍐呭鍜屽叧閿俊鎭? |
| **鐓х墖/鎻掑浘** | 涓讳綋瀵硅薄銆佸満鏅€佽瑙夌壒寰?| "鎻忚堪鍥剧墖涓殑涓昏鍐呭" |

- **鎻忚堪娉ㄥ叆鏂瑰紡**锛?
  - **鎺ㄨ崘锛氭敞鍏ユ鏂?*锛氬皢鐢熸垚鐨勬弿杩扮洿鎺ユ浛鎹㈡垨杩藉姞鍒?Chunk 姝ｆ枃涓殑鍥剧墖鍗犱綅绗︿綅缃紝鏍煎紡濡?`[鍥剧墖鎻忚堪: {caption}]`銆傝繖鏍锋弿杩颁細琚?Embedding 瑕嗙洊锛屽彲琚洿鎺ユ绱€?
  - **澶囬€夛細娉ㄥ叆 Metadata**锛氬皢鎻忚堪瀛樺叆 `chunk.metadata.image_captions` 瀛楁銆傞渶纭繚妫€绱㈡椂璇ュ瓧娈典篃琚储寮曘€?

- **骞傜瓑涓庡閲忓鐞?*锛?
  - 涓烘瘡寮犲浘鐗囩殑鎻忚堪璁＄畻鍐呭鍝堝笇锛屽瓨鍏?`processing_cache` 琛ㄣ€?
  - 閲嶅澶勭悊鏃讹紝鑻ュ浘鐗囧唴瀹规湭鍙樹笖 Prompt 鐗堟湰涓€鑷达紝鐩存帴澶嶇敤缂撳瓨鐨勬弿杩帮紝閬垮厤閲嶅璋冪敤 Vision LLM銆?

**4. Storage 闃舵锛氬弻杞ㄥ瓨鍌?*

- **鍚戦噺搴撳瓨鍌紙鐢ㄤ簬妫€绱級**锛?
  - 瀛樺偍澧炲己鍚庣殑 Chunk锛屽叾姝ｆ枃宸插寘鍚浘鐗囨弿杩帮紝Metadata 鍖呭惈 `image_refs` 鍒楄〃銆?
  - 妫€绱㈡椂閫氳繃鏂囨湰鐩镐技搴﹀嵆鍙懡涓寘鍚浉鍏冲浘鐗囨弿杩扮殑 Chunk銆?

- **鍘熷鍥剧墖瀛樺偍锛堢敤浜庤繑鍥烇級**锛?
  - 鍥剧墖鏂囦欢瀛樺偍浜庢湰鍦版枃浠剁郴缁燂紝璺緞璁板綍鍦ㄧ嫭绔嬬殑 `images` 绱㈠紩琛ㄤ腑銆?
  - 绱㈠紩琛ㄥ瓧娈碉細`image_id`, `file_path`, `source_doc`, `page`, `width`, `height`, `mime_type`銆?
  - 妫€绱㈠懡涓悗锛屾牴鎹?Chunk 鐨?`image_refs` 鏌ヨ绱㈠紩琛紝鑾峰彇鍥剧墖鏂囦欢璺緞鐢ㄤ簬杩斿洖銆?

#### 3.5.4 妫€绱笌杩斿洖娴佺▼

褰撶敤鎴锋煡璇㈠懡涓寘鍚浘鐗囩殑 Chunk 鏃讹紝绯荤粺闇€瑕佸皢鍥剧墖涓庢枃鏈竴骞惰繑鍥烇細

```
鐢ㄦ埛鏌ヨ: "绯荤粺鏋舵瀯鏄粈涔堟牱鐨勶紵"
    鈹?
    鈻?
Hybrid Search 鍛戒腑 Chunk锛堟鏂囧惈 "[鍥剧墖鎻忚堪: 绯荤粺閲囩敤涓夊眰鏋舵瀯...]"锛?
    鈹?
    鈻?
浠?Chunk.metadata.image_refs 鑾峰彇鍏宠仈鐨?image_id 鍒楄〃
    鈹?
    鈻?
鏌ヨ images 绱㈠紩琛紝鑾峰彇鍥剧墖鏂囦欢璺緞
    鈹?
    鈻?
璇诲彇鍥剧墖鏂囦欢锛岀紪鐮佷负 Base64
    鈹?
    鈻?
鏋勯€?MCP 鍝嶅簲锛屽寘鍚?TextContent + ImageContent
```

**MCP 鍝嶅簲鏍煎紡**锛?

```json
{
  "content": [
    {
      "type": "text",
      "text": "鏍规嵁鏂囨。锛岀郴缁熸灦鏋勫涓嬶細...\n\n[1] 鏉ユ簮: architecture.pdf, 绗?椤?
    },
    {
      "type": "image",
      "data": "<base64-encoded-image>",
      "mimeType": "image/png"
    }
  ]
}
```

#### 3.5.5 璐ㄩ噺淇濋殰涓庤竟鐣屽鐞?

- **鎻忚堪璐ㄩ噺妫€娴?*锛?
  - 瀵圭敓鎴愮殑鎻忚堪杩涜鍩虹璐ㄩ噺妫€鏌ワ紙闀垮害銆佹槸鍚﹀寘鍚叧閿俊鎭級銆?
  - 鑻ユ弿杩拌繃鐭垨 LLM 杩斿洖"鏃犳硶璇嗗埆"锛屾爣璁拌鍥剧墖涓?`low_quality`锛屽彲閫夋嫨浜哄伐澶嶆牳鎴栬烦杩囩储寮曘€?

- **澶у昂瀵?鐗规畩鍥剧墖澶勭悊**锛?
  - 瓒呭ぇ鍥剧墖鍦ㄤ紶鍏?Vision LLM 鍓嶈繘琛屽帇缂╋紙淇濇寔瀹介珮姣旓紝闄愬埗鏈€澶ц竟闀匡級銆?
  - 瀵逛簬绾楗版€у浘鐗囷紙濡傚垎闅旂嚎銆佽儗鏅浘锛夛紝鍙€氳繃灏哄鎴栦綅缃鍒欒繃婊わ紝涓嶈繘鍏ユ弿杩扮敓鎴愭祦绋嬨€?

- **鎵归噺澶勭悊浼樺寲**锛?
  - 鍥剧墖鎻忚堪鐢熸垚鏀寔鎵归噺寮傛璋冪敤锛屾彁楂樺悶鍚愰噺銆?
  - 鍗曚釜鏂囨。澶勭悊澶辫触鏃讹紝璁板綍澶辫触鐨勫浘鐗?ID锛屼笉褰卞搷鍏朵粬鍥剧墖鐨勫鐞嗚繘搴︺€?

- **闄嶇骇绛栫暐**锛?
  - 褰?Vision LLM 涓嶅彲鐢ㄦ椂锛岀郴缁熷洖閫€鍒?浠呬繚鐣欏浘鐗囧崰浣嶇"妯″紡锛屽浘鐗囦笉鍙備笌妫€绱絾涓嶉樆濉?Ingestion 娴佺▼銆?
  - 鍦?Chunk 涓爣璁?`has_unprocessed_images: true`锛屽悗缁彲澧為噺琛ュ厖鎻忚堪銆?

