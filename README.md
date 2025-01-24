# CADEL: Corpus of Administrative Web Documents for Japanese Entity Linking (Version 1.0)

## Overview

This Japanese entity linking dataset consists of 160 articles (subdocuments), primarily 
sourced from public relations magazines and white papers issued by Japanese government 
ministries and agencies. It includes manually annotated named and non-named mentions, 
their coreference relationships, and corresponding Wikidata entity IDs. Additionally, 
Wikipedia and OpenStreetMap entry IDs and geographic coordinates are automatically 
assigned via Wikidata entities.

## Data Statistics

The data statistics are as follows. 
Parts of a single source document are extracted and organized into one or more subdocuments.

You can confirm them using the following commmand (with Python 3.8.0 or later). For example,
- `python3 src/show_data_statistics.py -i data/json_split/train.json`

|                              |Train   |Dev     |Test   |Total| 
|--                            |--:     |--:     |--:    |--:  | 
|Document                      |      39|      15|     31|   85| 
|Subdocument                   |      74|      31|     55|  160| 
|Sentence                      |   1,607|     636|  1,609|3,852| 
|Mention                       |   2,903|   1,354|  3,825|8,082| 
|Mention w/ Wikidata link      |   2,123|   1,124|  3,215|6,462| 
|Mention w/ Wikipedia_Ja link  |   2,087|   1,115|  3,032|6,234| 
|Mention w/ OSM link	       |     613|     392|    974|1,979| 
|Mention related to Japan      |   1,846|     889|  2,203|4,938| 
|Entity                        |   1,472|     715|  1,852|4,039| 
|Entity w/ Wikidata link       |   1,041|     581|  1,508|2,994| 
|Entity w/ Wikipedia_Ja link   |   1,017|     572|  1,405|3,130| 
|Entity w/ OSM link            |     321|     182|    421|  924| 
|Entity related to Japan       |     884|     438|    967|2,289| 

The number of mentions for each entity type is as follows.
The names of persons not found in Wikidata are masked with `■` symbols, and their spans are annotated with the `PER_MASKED` type.
The `NOMINAL` type indicates non-named mentions, whereas the other types indicate named mentions.

|Type      |Explanation         |Train|Dev|Test|Total|
|--        |--                  |--:  |--:|--: |--:  |
|PER       |Person              |   41| 55| 125|  221|
|PER_MASKED|Person (masked)	|   44| 11|  31|   86|
|LIV	   |Living thinkgs	|    6|	 0|   2|    8|
|LOC	   |Location		|  813|329|1345|2,487|
|LOC-RIVER |Location:River	|   20| 37|  52|  109|
|FAC	   |Facility		|  289|173| 378|  840|
|FAC-LINE  |Facility:Line	|   83| 88|  48|  219|
|ORG	   |Organization	|  492|193| 634|1,319|
|PRO	   |Product		|  299|136| 238|  673|
|EVE	   |Event		|  184| 89| 198|  471|
|TIME	   |Time		|  235| 98| 173|  506|
|NOMINAL   |Nominal		|  397|145| 601|1,143|

The following entity types correspond to those in the [ATD-MCL dataset](https://github.com/naist-nlp/atd-mcl),
which focuses on geographic entity linking:
- `LOC` -> `LOC-NAME`
- `FAC` -> `FAC-NAME`
- `LOC-RIVER` & `FAC-LINE` -> `LINE-NAME`

## Data Format

### JSON

- A subdocument object value is assosiated with a key that represents the
  subdocument ID (e.g., 001-1). Each subdocument object has the sets of
  `metainfo`, `sentences`, `mentions`, and `entities`.
    ~~~~
    "001-1": {
      "metainfo": {
      ...
      },
      "sentences": {
      ...
      },
      "mentions": {
      ...
      },
      "entities": {
      ...
      }
    }
    ~~~~
- A metainfo object under `metainfo` is as follows:
    ~~~~
    "metainfo": {
      "src_date": "20221200",
      "src_url": "https://www.gsi.go.jp/common/000245996.pdf",
      "src_parent_url": "https://www.gsi.go.jp/kohokocho/koho654-top_00001.html"
    },
    ~~~~
- A sentence object under `sentences` is as follows
    ~~~~
    "sentences": {
      "001": {
        "type": "doc_title",
        "text": "国土地理院広報　2022年12月発行　第654号",
        "mention_ids": [
          "M001"
        ]
      },
      "002": {
        "type": "title",
        "text": "「令和4年度大規模津波防災総合訓練」に参加",
        "mention_ids": [
          "M002"
        ]
      },
      "003": {
        "text": "11月13日に高知県で南海トラフ地震を想定した大規模津波防災総合訓練が、国土交通省をはじめとする防災関係機関など107団体が参加して大規模に行われました。",
        "mention_ids": [
          "M003",
          "M004",
          "M005",
          "M006"
        ]
      },
      ...
    },
    ~~~~
- A mention object under `mentions` is as follows:
    ~~~~
    "mentions": {
      "M001": {
        "sentence_id": "001",
        "span": [
          0,
          7
        ],
        "text": "国土地理院広報",
        "entity_type": "PRO",
        "entity_id": "E001",
        "has_wikidata_ref": false,
        "has_jawiki_ref": false,
        "has_osm_ref": false
      },
      "M002": {
        "sentence_id": "002",
        "span": [
          1,
          17
        ],
        "text": "令和4年度大規模津波防災総合訓練",
        "entity_type": "EVE",
        "entity_id": "E002",
        "has_wikidata_ref": false,
        "has_jawiki_ref": false,
        "has_osm_ref": false
      },
      "M003": {
        "sentence_id": "003",
        "span": [
          7,
          10
        ],
        "text": "高知県",
        "entity_type": "LOC",
        "entity_id": "E003",
        "has_wikidata_ref": true,
        "has_jawiki_ref": true,
        "has_osm_ref": true
      },
      ...
    },
    ~~~~
- An entity object, which corresponds to a coreference cluster of one or 
  more mentions, under `entities` is as follows:
    ~~~~
    "entities": {
      "E001": {
        "member_mention_ids": [
          "M001"
        ],
        "entity_type_merged": "PRO"
        "has_wikidata_ref": false,
        "has_jawiki_ref": false,
        "has_osm_ref": false
      },
      "E002": {
        "member_mention_ids": [
          "M002",
          "M005"
        ],
        "entity_type_merged": "EVE"
        "has_wikidata_ref": false,
        "has_jawiki_ref": false,
        "has_osm_ref": false
        "ref_type": null,
        "ref_urls": {
          "other": "https://www.skr.mlit.go.jp/tsunamibousai2022/"
        },
      },
      "E003": {
        "member_mention_ids": [
          "M003",
          "M017",
          "M034",
          "M046"
        ],
        "entity_type_merged": "LOC"
        "has_wikidata_ref": true,
        "has_jawiki_ref": true,
        "has_osm_ref": true
        "ref_type": null,
        "ref_urls": {
          "wikidata": "https://www.wikidata.org/wiki/Q134093",
          "ja.wikipedia": "https://ja.wikipedia.org/wiki/%E9%AB%98%E7%9F%A5%E7%9C%8C",
          "openstreetmap": "https://www.openstreetmap.org/relation/3795031",
          "wikidata_country": "http://www.wikidata.org/entity/Q17"
        },
        "coordinate": [
          "33.559444444",
          "133.530833333"
        ],
      },
      ...
    }
    ~~~~

## Specification

- In each entity, null `ref_type` indicates an exact match link (一致リンク), while other values indicate non-exact match links (関連リンク) as defined in our paper.

## Copyright

The original authors retain the copyright of each original text.
The National Institute of Information and Communications Technology (NICT) retains the copyright of the annotation data.

## Data Sources of the Original Texts

See `suppl/data_sources.csv`.

## License

Academic Research Non-Commercial Limited CC-BY-NC-SA Reference-Type License (See `LICENSE`.)

## Change Log

- 2025/01/24: The Version 1.0 has been released.

## Citation

Please cite the following paper.

Japanese bibliography:
~~~~
@article{higashiyama-etal-2024-cadel,
    author  = "東山,翔平 and 出内,将夫 and 内山,将夫",
    title   = "日本語エンティティリンキングのための行政機関ウェブ文書コーパスの構築",
    journal = "情報処理学会研究報告",
    volume  = "2024-NL-260",
    number  = "10",
    pages   = "1--15",   
    year    = "2024",
    month   = "jun"
    url     = "https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=235101&item_no=1",
}
~~~~

English bibliography:
~~~~
@article{higashiyama-etal-2024-cadel,
    author  = "Shohei Higashiyama and Masao Ideuchi and Masao Utiyama",
    title   = "Construction of the Administrative Agency Web Document Corpus for {Japanese} Entity Linking [in {Japanese}]",
    journal = "IPSJ SIG Technical Report",
    volume  = "2024-NL-260",
    number  = "10",
    pages   = "1--15",   
    year    = "2024",
    month   = "jun",
    url     = "https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=235101&item_no=1",
}
~~~~
