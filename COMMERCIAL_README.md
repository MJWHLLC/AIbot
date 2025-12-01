Commercial Sale Notes and Preparation for Mobile App Distribution

This document explains the minimal steps to prepare the `paralegal_agent` codebase for sale as a mobile (phone) application. The repository is licensed under the MIT License, which permits commercial use, distribution, modification, and private use. However, there are additional legal, compliance, and operational steps you should take before packaging and selling a mobile app.

1) Licensing & Redistribution
- The MIT `LICENSE` in this folder grants permission to sell the software, so no additional license is required from the repository owner to enable sale.
- If you incorporate 3rd-party libraries that use different licenses, confirm their terms (some require attribution, others may restrict commercial use). See `requirements.txt` and each dependency's license.

2) Add an End-User License Agreement (EULA)
- For commercial distribution, include a EULA for end users. The EULA can be displayed at first run and should specify permitted uses, disclaimers, warranties, and limits of liability.
- Add `EULA.txt` or integrate EULA acceptance in the app UI/workflow before first use.

3) Privacy & Data Handling
- If the app collects or processes personal or sensitive data, prepare a Privacy Policy and ensure compliance with relevant laws (GDPR, CCPA, HIPAA if applicable).
- Host a stable privacy policy URL and include it in app store submission.

4) Attribution & Notices
- Preserve the `LICENSE` file inside the shipped package and include any required attribution for third-party libraries.

5) Packaging & Native Wrappers
- The current codebase is Python + Flask. To sell as a phone app you can:
  - Build a backend API (hosted) and create native mobile clients (iOS/Android) that talk to it.
  - Or embed the app in a mobile wrapper (e.g., use Kivy, BeeWare, or convert to a backend + WebView-based mobile shell). Server-hosting is recommended for security and updates.

6) App Store Submission
- For Apple App Store: follow Apple's guidelines, prepare privacy URL, EULA, screenshots, and app metadata.
- For Google Play Store: prepare privacy policy, target API level, and appropriate content ratings.

7) Commercial Terms & Billing
- Decide payment method: in-app purchases (Apple/Google), subscription billing, or external payments.
- If using in-app purchases for digital goods, follow each store's rules about handling payments.

8) Security & Compliance
- Ensure secrets (API tokens, SMTP passwords) are not bundled in the app binary. Use secure server-side storage.
- Add ephemeral tokens for client-server calls and secure HTTPS with TLS.

9) Branding & Trademarks
- If you plan to use trademarks or logos, ensure trademarks are registered/cleared.

10) Support & Updates
- Plan an update / support workflow. App stores require new builds for some changes, and you may want a server-side configuration to reduce full app updates.

11) Legal Review
- Before commercial distribution, consult with counsel to review licensing, liability, data protection, and claims about providing "paralegal" assistance — ensure disclaimers and attorney supervision clauses are clear.

12) Practical Steps to Ship
- Create a distribution branch and prepare a release build.
- Add `EULA.txt`, `PRIVACY.md`, and `ATTRIBUTION.md` to the repo.
- Create a release tag and assets (if needed) in GitHub.
- Host any server components on a secure provider (e.g., Azure, AWS) and set environment variables for production tokens.

This file is informational only and not a substitute for legal advice. Consult legal counsel for jurisdiction-specific steps and regulatory compliance.
