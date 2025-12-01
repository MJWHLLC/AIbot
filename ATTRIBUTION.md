# Attribution & Third-Party Licenses

**Paralegal Agent AI Bots**  
Copyright 2025 MJWHLLC. All rights reserved.

This document provides attribution and licensing information for third-party components used in this Software.

---

## 1. Open-Source Libraries

### 1.1 Python Core Dependencies

#### Flask
- **License:** BSD 3-Clause License
- **URL:** https://flask.palletsprojects.com/
- **Purpose:** Web framework for building the application
- **Copyright:** Copyright 2010 Pallets
- **Use:** Web server, routing, request handling

```
BSD 3-Clause License

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
```

#### Werkzeug
- **License:** BSD 3-Clause License
- **URL:** https://werkzeug.palletsprojects.com/
- **Purpose:** Password hashing, security utilities
- **Copyright:** Copyright 2010 Pallets
- **Use:** PBKDF2 password hashing, secure token generation

#### Flask-WTF
- **License:** BSD 3-Clause License
- **URL:** https://flask-wtf.readthedocs.io/
- **Purpose:** Form handling and CSRF protection
- **Copyright:** Copyright 2010 Pallets
- **Use:** CSRF token generation, form validation

#### Flask-Mail
- **License:** BSD 3-Clause License
- **URL:** https://pythonhosted.org/Flask-Mail/
- **Purpose:** Email sending functionality
- **Copyright:** Copyright 2010 Pallets
- **Use:** Email notifications, password reset emails

#### Requests
- **License:** Apache License 2.0
- **URL:** https://docs.python-requests.org/
- **Purpose:** HTTP client library
- **Copyright:** Copyright 2011 Kenneth Reitz
- **Use:** API calls to GitHub Models and external services

```
Apache License
Version 2.0, January 2004

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   "License" shall mean the terms and conditions for use, reproduction,
   and distribution as defined in Sections 1 through 9 of this document.

   "Licensor" shall mean the copyright owner or entity authorized by the
   copyright owner that is granting the License.

   "Derivative Works" shall mean any work, whether in source or object form,
   that is based on (or derived from) the Work.

   "Work" shall mean the work of authorship, made available under the License.
   A "Work" includes any and all portions of the Work.

2. Grant of Copyright License.

   Subject to the terms and conditions of this License, Licensor hereby
   grants to you a worldwide, non-exclusive, no-charge, royalty-free,
   irrevocable copyright license to reproduce, prepare Derivative Works of,
   and distribute copies of the Work.

3. Grant of Patent License.

   Subject to the terms and conditions of this License, Licensor hereby
   grants to you a worldwide, non-exclusive, no-charge, royalty-free,
   irrevocable patent license to make, have made, use, offer to sell, sell,
   import, and otherwise transfer the Work.
```

#### python-dotenv
- **License:** BSD 3-Clause License
- **URL:** https://github.com/theskumar/python-dotenv
- **Purpose:** Environment variable management
- **Copyright:** Copyright 2013 Saurabh Kumar
- **Use:** Loading .env configuration files

#### pytest
- **License:** MIT License
- **URL:** https://pytest.org/
- **Purpose:** Testing framework
- **Copyright:** 2004-2025 Holger Krekel and pytest contributors
- **Use:** Unit and integration tests

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
```

---

### 1.2 Development & CI/CD Dependencies

#### GitHub Actions
- **License:** MIT License (for public workflows)
- **URL:** https://github.com/features/actions
- **Purpose:** Continuous integration and deployment
- **Use:** Automated testing on push/PR

#### Docker
- **License:** Multiple (Docker CE: Community License)
- **URL:** https://www.docker.com/
- **Purpose:** Containerization platform
- **Use:** Container image building and deployment

---

## 2. External Services & APIs

### 2.1 GitHub Models API (Microsoft Azure)

- **Service:** GitHub Models hosted on Azure
- **Provider:** Microsoft Corporation
- **URL:** https://github.com/marketplace/models
- **Terms:** Governed by GitHub/Microsoft Terms of Service
- **Data:** Prompts sent to Azure for AI model inference
- **Models Supported:**
  - `gpt-4o-mini` (default, optimized for cost)
  - `gpt-4` (available with appropriate permissions)
  - `Claude 3.5 Sonnet` (if available)
  - `Llama 2` (if available)

**Important:** All data sent to GitHub Models is subject to Microsoft's Data Processing Addendum and Privacy Statement.

### 2.2 SMTP (Email Services)

- **Service:** User-configured SMTP server for email delivery
- **Provider:** Configurable (e.g., Gmail, Outlook, corporate mail server)
- **Terms:** Subject to email provider's privacy policy
- **Use:** Password resets, account notifications, legal document delivery

---

## 3. Standards & Specifications

### 3.1 Legal Standards & References

This Software references and implements:

- **Federal Rules of Civil Procedure (FRCP)**
  - Rules 4-6 (service, time, pleadings)
  - Rule 26 (general discovery)
  - Rule 56 (summary judgment)
  - Public domain; no attribution required
  - Source: U.S. Courts (https://www.uscourts.gov/)

- **Common Legal Document Templates**
  - Based on publicly available legal templates
  - Adapted for general educational use
  - Always consult an attorney for jurisdiction-specific requirements

---

## 4. Fonts & UI Resources

### 4.1 Bootstrap CSS Framework

- **License:** MIT License
- **URL:** https://getbootstrap.com/
- **Purpose:** Responsive UI framework (if used in templates)
- **Copyright:** 2011-2025 Twitter, Inc. and Bootstrap contributors

### 4.2 Font Awesome (if used)

- **License:** Multiple (CC BY 4.0 for free icons, proprietary for pro icons)
- **URL:** https://fontawesome.com/
- **Purpose:** Icon library (if used in templates)

---

## 5. Documentation & Learning Resources

### 5.1 Sources Referenced in Documentation

- **Python Official Documentation:** https://docs.python.org/ (CC0 1.0)
- **Flask Documentation:** https://flask.palletsprojects.com/
- **GitHub Documentation:** https://docs.github.com/ (CC-BY-4.0)
- **StackOverflow:** Community-contributed solutions
- **W3C Standards:** HTML5, CSS3 specifications

---

## 6. How to Contribute & Attribution

If you modify this Software and redistribute it:

1. **Retain Notices:** Keep all copyright, license, and attribution notices
2. **License Compliance:** If using open-source components, comply with their licenses
3. **Document Changes:** Create a CHANGELOG documenting modifications
4. **Provide Source:** If distributing binary or modified versions, provide access to source code as required by licenses
5. **Credits:** Give credit to MJWHLLC and contributors

### Contributing Guidelines

Contributions are welcome! By contributing, you agree that:

- Your contributions will be licensed under the same terms as this project
- You retain copyright to your contributions
- You grant MJWHLLC a royalty-free, worldwide license to use, modify, and distribute your contributions

---

## 7. License Compatibility Summary

| Component | License | Compatibility | Commercial Use |
|-----------|---------|----------------|-----------------|
| Flask | BSD 3-Clause | ✅ Permissive | ✅ Allowed |
| Werkzeug | BSD 3-Clause | ✅ Permissive | ✅ Allowed |
| Flask-WTF | BSD 3-Clause | ✅ Permissive | ✅ Allowed |
| Flask-Mail | BSD 3-Clause | ✅ Permissive | ✅ Allowed |
| Requests | Apache 2.0 | ✅ Permissive | ✅ Allowed |
| python-dotenv | BSD 3-Clause | ✅ Permissive | ✅ Allowed |
| pytest | MIT | ✅ Permissive | ✅ Allowed |
| Paralegal Agent | MIT | ✅ Permissive | ✅ Allowed |

**Summary:** All dependencies use permissive licenses compatible with commercial distribution.

---

## 8. No Warranty for Third-Party Components

THIS SOFTWARE INCLUDES THIRD-PARTY COMPONENTS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE AUTHORS OF THIRD-PARTY COMPONENTS ARE NOT LIABLE FOR ANY DAMAGES ARISING FROM THEIR USE.

See EULA.txt and PRIVACY.md for full warranty disclaimers.

---

## 9. Legal Compliance

When using this Software with third-party components:

- **GDPR Compliance:** Third-party services may process EU data; ensure DPA compliance
- **CCPA Compliance:** Disclose third-party data sharing in privacy policies
- **HIPAA:** If handling protected health information, ensure Business Associate Agreements
- **SOC 2:** Verify third-party service SOC 2 compliance if required

---

## 10. How to Report Attribution Issues

If you discover:

- Missing attribution for a third-party component
- Incorrect license information
- License compliance violations
- Copyright concerns

Please report to: [your contact email]

**Include:**
- Component name and version
- License or attribution information
- Your suggested correction
- Any relevant documentation

---

## 11. Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-30 | 1.0 | Initial ATTRIBUTION.md |

---

## 12. Contact & Support

For licensing questions, commercial inquiries, or attribution corrections:

**Company:** MJWHLLC  
**Email:** [your contact email]  
**Website:** [your website]  
**GitHub:** https://github.com/MJWHLLC/AIbot

---

**Thank you to all open-source contributors and community members who make this Software possible!**

---

*Last Updated: November 30, 2025*  
*This document is part of Paralegal Agent AI Bots and is distributed under the MIT License.*
