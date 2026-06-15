import pandas as pd
import numpy as np
import tldextract
import re
import urllib.parse
import math
from collections import Counter
from tqdm import tqdm
 
def shannon_entropy(s):
    if not s:
        return 0
    freq = Counter(s)
    probs = [f / len(s) for f in freq.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

 
def extract_all_features(url, label=None):

    if not re.match(r'http(s)?://', url):
        url = "http://" + url

    try:
        parsed = urllib.parse.urlparse(url)
        ext = tldextract.extract(url)

        domain = ext.registered_domain or ""
        subdomain = ext.subdomain or ""
        tld = ext.suffix or ""
        path = parsed.path or ""

        raw_digits = sum(ch.isdigit() for ch in url)
        raw_uppercase = sum(ch.isupper() for ch in url)

        features = {}

         
         
        features['domain_length'] = len(domain)
        features['subdomain_length'] = len(subdomain)
        features['tld_length'] = len(tld)

         
         
        features['count_dots'] = url.count('.')
        features['count_hyphens'] = url.count('-')
        features['count_underscores'] = url.count('_')
        features['count_letters'] = sum(ch.isalpha() for ch in url)
        features['count_digits'] = raw_digits   # IMPORTANT FIX

        safe_len = len(url) if len(url) > 0 else 1
        features['ratio_digits'] = raw_digits / safe_len
        features['ratio_uppercase'] = raw_uppercase / safe_len

        vowels = sum(url.lower().count(v) for v in 'aeiou')
        features['vowel_ratio'] = vowels / max(features['count_letters'], 1)

         
         
        tokens = re.split(r'\W+', url)
        tokens = [t for t in tokens if t]

        features['avg_token_len'] = np.mean([len(t) for t in tokens]) if tokens else 0
        features['max_token_len'] = np.max([len(t) for t in tokens]) if tokens else 0

         
         
        features['char_entropy'] = shannon_entropy(url)

         
         
        features['has_https'] = int(parsed.scheme == "https")

        suspicious_keywords = [
            'login','verify','account','secure','bank',
            'paypal','admin','support','update','signin'
        ]

        features['suspicious_in_path'] = int(any(w in path.lower() for w in suspicious_keywords))
        features['suspicious_in_subdomain'] = int(any(w in subdomain.lower() for w in suspicious_keywords))
        features['suspicious_in_domain'] = int(any(w in domain.lower() for w in suspicious_keywords))

         
         
        if label is not None:
            features['label'] = label

    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

    return features


 
 
if __name__ == "__main__":

    INPUT_FILE = "master_url_dataset_enriched.csv"
    OUTPUT_FILE = "features_dataset.csv"

    df = pd.read_csv(INPUT_FILE)
    df = df.dropna(subset=['url'])

    all_features = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        f = extract_all_features(row['url'], row['label'])
        if f:
            all_features.append(f)

    df_feat = pd.DataFrame(all_features).fillna(0)

    cols = [c for c in df_feat.columns if c != 'label']
    cols.sort()
    df_feat = df_feat[cols + ['label']]

    df_feat.to_csv(OUTPUT_FILE, index=False)

    print("✅ Feature extraction complete")