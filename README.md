# dkim-splitter 🔑

A simple, CLI tool to split long **DKIM TXT records** into
**255-character chunks** for AWS Route 53 (or any DNS provider that enforces
the DNS TXT record length limit).

---

## 🚀 Why?

- **DNS protocol limitation**: TXT records cannot exceed **255 characters per
  string** (RFC 1035).
- **DKIM public keys** are usually much longer than 255 characters.
- **AWS Route 53** (and other DNS providers) enforce this strictly, so you
  cannot paste a DKIM key as one giant string.
- The solution: split the key into multiple quoted strings, each ≤255 chars,
  and DNS will concatenate them automatically.

This tool makes it **easy and foolproof**.

---

## ✨ Features

- Split any DKIM key into **RFC-compliant 255-char chunks**
- Output in **Route 53–ready format** (`"..." "..."`)
- Works with **stdin**, **file input**, or **direct argument**
- Optional **output to file**
- **Validation**: warns if any chunk >255 chars
- **Friendly UX** with clear ✅/❌ messages
- **Quiet mode** for scripting

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/Paul1404/dkim-splitter.git
cd dkim-splitter
```

Run directly with Python:

```bash
python3 dkim_splitter.py
```

(Optional) Install globally:

```bash
pip install .
```

Then you can run it anywhere as:

```bash
dkim-splitter
```

---

## 🛠 Usage

### 1. Interactive (stdin)

```bash
python3 dkim_splitter.py
```

Paste your DKIM key (one line, no quotes):

```
v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
```

Output:

```
✅ Route 53–ready DKIM record:

"v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..." "restOfKeyHere..."

📋 Copy & paste this into Route 53 TXT record value field.
ℹ️  Total length: 420 chars
ℹ️  Split into 2 chunks (max 255 chars each)
```

---

### 2. From file

```bash
python3 dkim_splitter.py -f dkim.txt
```

---

### 3. Direct argument

```bash
python3 dkim_splitter.py "v=DKIM1; k=rsa; p=MIIBIjANBg..."
```

---

### 4. Save to file

```bash
python3 dkim_splitter.py -f dkim.txt -o split.txt
```

---

### 5. Quiet mode (for scripting)

```bash
python3 dkim_splitter.py -f dkim.txt -q
"v=DKIM1;..." "restOfKey..."
```

---

## 🔍 Verification

After publishing your DKIM record in Route 53, verify with:

```bash
dig TXT dkim._domainkey.example.com
```

You should see the **full DKIM key as one continuous string**.

Or send a test email to [DKIM Validator](https://dkimvalidator.com/) to confirm
your DKIM signature is valid.

---

## 📜 License

MIT License © 2025 [Paul Dresch](https://github.com/Paul1404)