# Digital & Remote Banking Security Architecture
**Document ID:** SEC-DIG-2026-09  
**Applies To:** Mobile App, Web Banking, Remote Deposit Capture, Multi-Factor Systems  
**Compliance Standard:** FFIEC Cybersecurity Assessment Tool / NIST SP 800-63B  

---

## 1. Remote Check Deposit (RDC) Operational Controls
To prevent duplicate presentment and check fraud, account holders leveraging mobile deposit capture must adhere to strict processing criteria:

1. **Restrictive Physical Endorsement Mandate:**  
   Every item submitted via Remote Deposit Capture must bear the account holder's physical ink signature and the explicit phrase:  
   *“For Mobile Deposit Only at Apex Financial — Account # [Last 4 digits]”*  
   Deposits missing this restrictive endorsement are subject to immediate algorithmic rejection.
2. **Clearing Thresholds and Cutoff Times:**
   * Business-day cutoff for same-day processing is **5:00 PM Eastern Time**.
   * First $\$225.00$ made available next business day. Remaining funds released within two (2) business days barring automated fraud verification holds.
3. **Ineligible Instruments:** Third-party checks, altered checks, money orders, checks drawn on foreign financial institutions, and traveler's checks are barred from RDC submission.

---

## 2. Multi-Factor Authentication (MFA) Standards
Apex Financial enforces continuous authentication profiles to secure member assets:

```
+------------------------------------------------------------------------------------+
|                         AUTHENTICATION INTEGRITY LEVELS                            |
+----------------------+--------------------+----------------------------------------+
| Interaction Level    | Security Profile   | Approved Modalities                    |
+----------------------+--------------------+----------------------------------------+
| Standard Portal Sign | Tier 1 (Moderate)  | Password + Biometric / Push Token      |
| Wire / High-Value Tx | Tier 2 (Elevated)  | FIDO2 WebAuthn / Time-based OTP (TOTP) |
| Credential / KYC Mod | Tier 3 (Maximum)   | Biometric Verification + Hardware Key  |
+----------------------+--------------------+----------------------------------------+
```

* **Prohibited Channels:** Delivery of one-time authentication codes via unsecured SMS is disabled by default for sensitive fund movements and credential management due to SIM-swapping vulnerabilities.

---

## 3. Account Takeover (ATO) Mitigation Protocols
* **Adaptive Risk Profiling:** The banking portal continuously parses device fingerprinting, IP geofencing, mouse movement metrics, and typing cadence. Anomalous activities automatically lock out transactional access until dual verification is finalized.
* **Cooling-Off Quarantine:** Any change to an account holder's registered mobile number, email address, or physical address automatically places a 24-hour hold on outbound peer-to-peer transfers, wire services, and remote limit-increase authorizations.
* **Fraud Reporting SLAs:** Account holders who suspect unauthorized digital access must immediately engage the 24/7 Apex Incident Desk. Unauthorized electronic fund transfers covered under Regulation E require verbal or written notice within sixty (60) days of the transmittal of the periodic statement.