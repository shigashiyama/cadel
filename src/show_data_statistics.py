import argparse
from collections import Counter
import json
import sys


def load_json(
        input_path: str,
) -> dict:

    with open(input_path, encoding='utf-8') as f:
        print(f'Read: {input_path}', file=sys.stderr)
        data = json.load(f)
    return data


def write_as_json(
        data: dict,
        output_path: str,
) -> None:

    with open(output_path, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, ensure_ascii=False, indent=2)
    print(f'Saved: {output_path}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_json_paths', '-i',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--reference_json_paths', '-r',
        type=str,
    )
    args = parser.parse_args()

    data = {}
    for input_path in args.input_json_paths.split(','):
        data_tmp = load_json(input_path)
        data.update(data_tmp)

    ref_data = {}
    if args.reference_json_paths:
        for ref_path in args.reference_json_paths.split(','):
            data_tmp = load_json(ref_path)
            ref_data.update(data_tmp)
    
    # show statistics
    counter = Counter()
    doc_set = set()
    key2sets = {'num_mens': set()}

    for subdoc_id, doc in data.items():
        counter['num_subdocs'] += 1

        doc_id = subdoc_id.split('-')[0]
        doc_set.add(doc_id)

        if 'sections' in doc:
            counter['num_secs'] += len(doc['sections'])

        if 'sentences' in doc:
            counter['num_sens'] += len(doc['sentences'])

        if 'mentions' in doc:
            counter['num_mens'] += len(doc['mentions'])

            for men_id, men in doc['mentions'].items():
                key2sets['num_mens'].add(men['text'])

                if 'entity_type' in men:
                    key = f'num_mens:{men["entity_type"]}'
                    counter[key] += 1
                    if not key in key2sets:
                        key2sets[key] = set()
                    key2sets[key].add(men['text'])

                    if men['entity_type'].endswith('NAME'):
                        counter[f'num_mens:has_name'] += 1

                if 'has_wikidata_ref' in men and men['has_wikidata_ref']:
                    counter['num_mens:has_wd_ref'] += 1
                if 'has_jawiki_ref' in men and men['has_jawiki_ref']:
                    counter['num_mens:has_jawiki_ref'] += 1
                if 'has_osm_ref' in men and men['has_osm_ref']:
                    counter['num_mens:has_osm_ref'] += 1

                ent = doc['entities'][men['entity_id']]
                if ('ref_urls' in ent
                    and 'wikidata_country' in ent['ref_urls']
                    and ent['ref_urls']['wikidata_country'].endswith('/Q17')
                ):
                    counter['num_mens:is_japan'] += 1

        if 'entities' in doc:
            counter['num_ents'] += len(doc['entities'])

            for ent_id, ent in doc['entities'].items():
                if 'has_wikidata_ref' in ent and ent['has_wikidata_ref']:
                    counter['num_ents:has_wd_ref'] += 1
                if 'has_jawiki_ref' in ent and ent['has_jawiki_ref']:
                    counter['num_ents:has_jawiki_ref'] += 1
                if 'has_osm_ref' in ent and ent['has_osm_ref']:
                    counter['num_ents:has_osm_ref'] += 1
                if ('ref_urls' in ent
                    and 'wikidata_country' in ent['ref_urls']
                    and ent['ref_urls']['wikidata_country'].endswith('/Q17')
                ):
                    counter['num_ents:is_japan'] += 1

                has_name = False
                for men_id in ent['member_mention_ids']:
                    men = doc['mentions'][men_id]
                    if men['entity_type'].endswith('NAME'):
                        has_name = True

                if has_name:
                    counter['num_ents:has_name'] += 1

    counter['num_docs'] = len(doc_set)

    print('\n#Data statistics.\n#key\ttotal\t(unique)')
    main_keys = ['num_docs', 'num_subdocs', 'num_sens', 'num_mens', 'num_ents']
    for key in main_keys:
        val = counter[key]
        if key in key2sets:
            val2 = len(key2sets[key])
            print(f'{key}\t{val}\t({val2})')
        else:
            print(f'{key}\t{val}')
        
    for key, val in sorted(counter.items()):
        if not key in main_keys:
            if key in key2sets:
                val2 = len(key2sets[key])
                print(f'{key}\t{val}\t({val2})')
            else:
                print(f'{key}\t{val}')

    if ref_data:        
        ref_mention_wd_set = set()
        ref_mention_wp_set = set()
        ref_mention_osm_set = set()

        mention_wd_all = mention_wd_known = 0
        mention_wp_all = mention_wp_known = 0
        mention_osm_all = mention_osm_known = 0

        for subdoc_id, doc in ref_data.items():
            for men_id, men in doc['mentions'].items():
                men_text = men['text']
                ent = doc['entities'][men['entity_id']]
                
                if ent['has_wikidata_ref']:
                    wd_url = ent['ref_urls']['wikidata']
                    ref_mention_wd_set.add((men_text, wd_url))
             
                if ent['has_jawiki_ref']:
                    wp_url = ent['ref_urls']['ja.wikipedia']
                    ref_mention_wp_set.add((men_text, wp_url))
             
                if ent['has_osm_ref']:
                    osm_url = ent['ref_urls']['openstreetmap']
                    ref_mention_osm_set.add((men_text, osm_url))

        for subdoc_id, doc in data.items():
            for men_id, men in doc['mentions'].items():
                men_text = men['text']
                ent = doc['entities'][men['entity_id']]
                
                if ent['has_wikidata_ref']:
                    wd_url = ent['ref_urls']['wikidata']
                    key = (men_text, wd_url)
                    mention_wd_all += 1
                    if key in ref_mention_wd_set:
                        mention_wd_known += 1
             
                if ent['has_jawiki_ref']:
                    wp_url = ent['ref_urls']['ja.wikipedia']
                    key = (men_text, wp_url)
                    mention_wp_all += 1
                    if key in ref_mention_wp_set:
                        mention_wp_known += 1
             
                if ent['has_osm_ref']:
                    osm_url = ent['ref_urls']['openstreetmap']
                    key = (men_text, osm_url)
                    mention_osm_all += 1
                    if key in ref_mention_osm_set:
                        mention_osm_known += 1
                           
        print('\n#Instance statistics. (instance: a pair of a mention text and its link)')
        print('#num_all_ins\tratio_unknown_ins')
        print(f'WD:\t{mention_wd_all}\t{(mention_wd_all-mention_wd_known)/mention_wd_all:.2f}')
        print(f'JWP:\t{mention_wp_all}\t{(mention_wp_all-mention_wp_known)/mention_wp_all:.2f}')
        print(f'OSM:\t{mention_osm_all}\t{(mention_osm_all-mention_osm_known)/mention_osm_all:.2f}')


if __name__ == '__main__':
    main()
