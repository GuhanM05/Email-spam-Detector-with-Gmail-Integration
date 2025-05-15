
def extract_features(email_text, sender_email=None):
    import re
    from urllib.parse import urlparse

    features = {}

    # Number of links
    features['num_links'] = len(re.findall(r'http[s]?://', email_text))

    # Suspicious words
    suspicious_keywords = ['free', 'urgent', 'winner', 'act now', 'money', 'guarantee']
    features['suspicious_words'] = sum(1 for word in suspicious_keywords if word in email_text.lower())

    # Structure-based features
    features['has_attachment'] = int('attachment' in email_text.lower())
    features['reply_to_mismatch'] = int('reply-to:' in email_text.lower() and 'from:' in email_text.lower())

    # Metadata (simulated)
    features['subject_length'] = len(email_text.splitlines()[0]) if email_text else 0
    features['sender_reputation'] = sender_reputation_score(sender_email or "")

    return features

def sender_reputation_score(sender_email):
    domain = sender_email.split('@')[-1] if '@' in sender_email else ''
    trusted_domains = ['gmail.com', 'outlook.com', 'yahoo.com']
    if domain in trusted_domains:
        return 1.0
    elif domain.endswith('.ru') or domain.endswith('.xyz'):
        return 0.2
    return 0.5
