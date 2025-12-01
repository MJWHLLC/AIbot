# Privacy Policy

**Paralegal Agent AI Bots**  
Copyright 2025 MJWHLLC. All rights reserved.

**Last Updated:** November 30, 2025  
**Effective Date:** November 30, 2025

---

## 1. Introduction

This Privacy Policy ("Policy") describes how Paralegal Agent AI Bots ("Software," "Service," or "Company") collects, uses, shares, and protects information about you when you use the Software.

**Important:** This Software is intended for law firms, legal professionals, and authorized users only. By using this Software, you acknowledge and agree to the terms of this Privacy Policy.

---

## 2. Information We Collect

### 2.1 User-Provided Information

When you use the Software, we may collect:

- **Account Information:** Name, email address, password (hashed), organization/firm name
- **User Profile Data:** Role (user/admin), preferences, authentication tokens
- **Document Data:** Legal documents you create, drafts, research queries, case information
- **Communication Data:** Email addresses for password resets, account notifications, email delivery logs
- **Login/Session Data:** Username, login timestamps, session tokens, IP addresses (if server-based)

### 2.2 Automatically Collected Information

- **Usage Data:** Features accessed, document types generated, query frequency, timestamps
- **Device/System Information:** Browser type, operating system (for web deployments), screen resolution
- **Error Logs:** Application errors, debugging information, stack traces
- **AI Model Interactions:** Prompts submitted (for model training/improvement if enabled)

### 2.3 Optional Data

- **SMTP Configuration:** Email server settings (username, encrypted password) for notification delivery
- **External API Tokens:** GitHub Models API tokens (stored encrypted, never logged in plain text)
- **File Uploads:** Any documents or attachments you voluntarily upload

---

## 3. How We Use Your Information

We use collected information for:

1. **Service Delivery:** Operating the Software, generating legal documents, processing user queries
2. **Authentication & Authorization:** User login, session management, access control
3. **Communication:** Sending password resets, notifications, account updates
4. **Improvement & Analytics:** Understanding feature usage, optimizing performance, fixing bugs
5. **Legal Compliance:** Complying with applicable laws, enforcing this Policy and our Terms
6. **Security:** Detecting fraud, preventing unauthorized access, protecting against misuse

---

## 4. Data Storage & Security

### 4.1 Local Deployment (On-Premises)

- **Location:** Data stored on your local server or computer
- **Responsibility:** You are responsible for backup, security, and compliance with data protection laws
- **Access:** Only users with local system access can access the database
- **Encryption:** Passwords stored using industry-standard hashing (Werkzeug default: PBKDF2)

### 4.2 Cloud Deployment

- **Storage:** If deployed on cloud infrastructure, data may be stored on that provider's servers
- **Provider Responsibility:** Cloud provider's privacy policy applies in addition to this Policy
- **Data Residency:** You control which region/data center stores your data

### 4.3 AI Model Interactions

- **GitHub Models API:** Prompts and queries are sent to Microsoft Azure for processing
- **Data Retention:** GitHub Models API may retain prompts/responses per Microsoft's Data Protection Addendum
- **No Local Storage:** AI model outputs are not automatically stored unless you save them
- **Recommendation:** Do not include personally identifiable information (PII) or confidential client data in AI queries

### 4.4 Security Measures

We implement:

- **Password Hashing:** Passwords hashed using PBKDF2-SHA256 (minimum 100,000 iterations)
- **Session Tokens:** Cryptographically secure token generation (secrets module)
- **CSRF Protection:** CSRF tokens on all state-changing forms (Flask-WTF)
- **SQL Injection Prevention:** Parameterized queries (SQLite3)
- **HTTPS Support:** SSL/TLS encryption recommended for all deployments
- **Environment Variables:** Sensitive credentials (API tokens) isolated from code

---

## 5. Data Sharing & Disclosure

### 5.1 Third Parties

We do NOT share user data with third parties except:

- **AI Model Providers (Microsoft/GitHub):** Prompts sent to Azure for processing
- **Email Providers:** If SMTP is configured, email addresses sent to your mail server
- **Legal Requirements:** If required by law, court order, or government request
- **Service Providers:** Any hosting or infrastructure partners you choose

### 5.2 User Control

You retain full control over:

- Enabling/disabling email notifications
- Sharing specific documents with other users (admin-controlled)
- Configuring API tokens and external integrations
- Exporting or deleting your data

---

## 6. Data Retention

- **Active Accounts:** Data retained while your account is active
- **Account Deletion:** Upon request, all account data deleted (manual process)
- **Documents:** Retained until you delete them or request full data purge
- **Server Logs:** Application logs retained for 30 days (configurable)
- **Backups:** Backups may contain data for up to 90 days

---

## 7. Your Rights & Choices

Depending on your jurisdiction, you may have rights to:

- **Access:** Request a copy of your personal data
- **Correction:** Correct inaccurate or incomplete data
- **Deletion:** Request deletion of your data (with exceptions for legal requirements)
- **Portability:** Receive your data in a portable format
- **Opt-Out:** Disable email notifications or data collection features
- **Restriction:** Limit how your data is processed

To exercise these rights, contact: [your contact email]

---

## 8. Children's Privacy

This Software is NOT intended for use by children under 13 years old. We do not knowingly collect information from children under 13. If we become aware of such collection, we will delete it promptly.

---

## 9. Cookies & Tracking

- **Session Cookies:** Flask session cookies used for authentication (expires with browser session)
- **Persistent Cookies:** Optional "remember me" tokens (configurable, 30-day TTL)
- **Tracking:** No third-party analytics or tracking services by default
- **Your Control:** You can disable cookies in your browser; note that this may limit Software functionality

---

## 10. International Data Transfers

If data is transferred internationally:

- **Compliance:** We comply with applicable data transfer regulations (e.g., GDPR Standard Contractual Clauses, CCPA)
- **Third Parties:** Third-party providers (Microsoft/GitHub) are responsible for compliance
- **Contact Us:** For details on safeguards, contact [your contact email]

---

## 11. Data Protection Compliance

### 11.1 GDPR (European Users)

If you are a resident of the European Union, you have rights under GDPR including:
- Right to access, rectification, erasure, restriction of processing, portability, objection
- Right to lodge a complaint with a supervisory authority
- Legal basis for processing: Consent, legitimate interest, contract performance, legal obligation

### 11.2 CCPA (California Users)

If you are a California resident, you have rights under CCPA including:
- Right to know, delete, opt-out of sale/sharing, and limit use
- Right not to be discriminated against for exercising rights
- Shine the Light request capability

### 11.3 PIPEDA (Canadian Users)

If you are a Canadian resident, you have rights under PIPEDA including:
- Right to access, correction, privacy complaint resolution

---

## 12. Third-Party Links & Services

This Software may integrate with third-party services:

- **GitHub Models API:** Governed by Microsoft's Privacy Statement
- **Email Services:** Governed by your SMTP provider's Privacy Policy
- **Cloud Hosting:** Governed by your hosting provider's Privacy Policy

We are NOT responsible for third-party privacy practices. Review their policies before use.

---

## 13. Security Incidents

If a security breach occurs:

- **Notification:** We will notify affected users as required by law (typically within 30 days)
- **Details:** Notification will include nature of breach, data affected, steps taken to remediate
- **Contact:** Affected users will be notified via email or in-app notification

---

## 14. Changes to This Policy

We reserve the right to update this Privacy Policy at any time. Changes are effective upon posting. Continued use after changes constitutes acceptance.

- **Version History:** Changes logged below
- **Notice:** Material changes will be communicated via email or in-app notification

---

## 15. Contact & Data Protection Officer

For privacy questions, data subject requests, or to report concerns:

**Company:** MJWHLLC  
**Email:** [your contact email]  
**Website:** [your website]  
**Mailing Address:** [your mailing address]  

---

## 16. Legal Compliance Notice

**IMPORTANT:** This Software is designed for legal professionals only. It provides tools for legal research, document drafting, and case management. The output is NOT a substitute for professional legal counsel.

- **No Attorney-Client Privilege:** Communications with this Software do NOT create an attorney-client relationship
- **No Legal Advice:** This Software does not provide legal advice and should not be relied upon as such
- **Professional Consultation:** Always consult with a qualified attorney before taking legal action

---

## 17. Acceptable Use

By using this Software, you agree NOT to:

- Use it to generate documents for unlawful purposes
- Violate applicable legal ethics rules or bar association regulations
- Disclose confidential client information through insecure channels
- Use it in any manner that infringes on intellectual property rights
- Attempt to gain unauthorized access to systems or data

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-30 | 1.0 | Initial Privacy Policy |

---

**End of Privacy Policy**

By using Paralegal Agent AI Bots, you acknowledge that you have read and understood this Privacy Policy and agree to be bound by its terms.
