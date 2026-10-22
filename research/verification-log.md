# Verification log — SAVINGS2

All retrieval timestamps are **2026-10-22 (UTC)**. Each entry records the exact wording read on the cited official page
and the value that was written into `data/banks.json`. Where a page would not disclose a value, the entry says so and the
field is blank in the dataset.

Legend: ✅ verified · ⚠️ partial (value exists but cannot be tied to a dated, complete official statement) · ⛔ unverified / blank

---

## 1. FDIC institution checks (via api.fdic.gov, index `institutions_20261016090006`, created 2026-10-16)

Query used: `https://api.fdic.gov/banks/institutions?filters=...&fields=NAME,CERT,ACTIVE,STALP,ASSET,WEBADDR`

| Bank (legal entity) | CERT | ACTIVE | State | Result |
| --- | --- | --- | --- | --- |
| JPMorgan Chase Bank, National Association | 628 | 1 | OH | ✅ active |
| Bank of America, National Association | 3510 | 1 | NC | ✅ active |
| Citibank, National Association | 7213 | 1 | SD | ✅ active |
| Wells Fargo Bank, National Association | 3511 | 1 | SD | ✅ active |
| Goldman Sachs Bank USA | 33124 | 1 | NY | ✅ active |
| U.S. Bank National Association | 6548 | 1 | OH | ✅ active |
| Capital One, National Association | 4297 | 1 | VA | ✅ active |
| PNC Bank, National Association | 6384 | 1 | DE | ✅ active |
| Truist Bank | 9846 | 1 | NC | ✅ active |
| TD Bank, National Association | 18409 | 1 | DE | ✅ active |
| Citizens Bank, National Association | 57957 | 1 | RI | ✅ active |
| American Express National Bank | 27471 | 1 | UT | ✅ active |
| Ally Bank | 57803 | 1 | UT | ✅ active |
| SoFi Bank, National Association | 26881 | 1 | UT | ✅ active |
| First-Citizens Bank & Trust Company (CIT Bank division) | 11063 | 1 | NC | ✅ active |
| HSBC Bank USA, National Association | 57890 | 1 | VA | ✅ active |
| Fifth Third Bank, National Association | 6672 | 1 | OH | ✅ active |
| Barclays Bank Delaware | 57203 | 1 | DE | ✅ active |
| **Discover Bank** | **5649** | **0** | DE | ⛔ **inactive** — recorded as merged; not counted as a separate $250k capacity |

Note on units: the API's `ASSET` field is reported in thousands of dollars. It was used only to rank institutions by size
for the initial screen; no asset figure is published on the site.

---

## 2. Product-by-product verification

### Chase Savings℠ — JPMorgan Chase Bank, N.A. (CERT 628) — ⛔ APY blank

| Field | Value recorded | Evidence (official page) | URL |
| --- | --- | --- | --- |
| APY | **blank** | Page: *"In order to see rates table, please provide valid 5-digit zip code."* Submitting `?zipCode=10001` did not render a table. FAQ: *"Website rates are generally updated each business day in the morning and may vary by market."* | https://www.chase.com/personal/savings/savings-account/interest-rates |
| Minimum to open | $0 | FAQ: *"Chase Savings℠ does not require a minimum balance to open."* | https://www.chase.com/personal/savings/savings-account |
| Monthly fee | $5 | *"$5 or $0 fee with a balance at the beginning of each day of $300 or more in this account each monthly statement period."* | same |
| Fee waiver ways | recorded | $300 beginning-of-day balance; $25+ Autosave/recurring transfers from a Chase checking account; linked qualifying checking account; owner under 25 | same |
| App | Chase Mobile® | *"Deposit checks and transfer money to your savings from virtually anywhere, all with the Chase Mobile® app."* | same |
| Security | recorded | *"we encrypt your data"*; *"Our app supports Apple TouchID, FaceID and Android's fingerprint or facial recognition login"*; *"passkey and password manager enabled"*; *"additional validation checks like mobile app notifications or a one-time code"*; *"24/7"* fraud monitoring | https://www.chase.com/digital/resources/privacy-security |
| FDIC | recorded | *"Chase savings accounts are FDIC insured up to the maximum amount allowed by law."* | product page |
| Opening rules | recorded | FAQ: online at chase.com or in a branch; address, email, SSN and contact details | product page |

### Bank of America Advantage Savings — Bank of America, N.A. (CERT 3510) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | Not present in the served HTML; the product page carries no rate text and no rate endpoint resolved (`/deposits/savings/savings-accounts/rates/` → "page you're trying to reach is not available"). | https://www.bankofamerica.com/deposits/savings/savings-accounts/ |
| Monthly fee | **blank** | Page renders literal placeholders: *"$XXXX or $0"* and *"You maintain a minimum daily balance of $XXXX or more"*. | same |
| Fee waiver conditions | recorded (no amounts) | minimum daily balance; Advantage Relationship Banking; BofA Rewards Preferred Plus / Preferred Honors / Premier; owner under 25 | same |
| App | Bank of America app | App Store and Google Play download links published on the page | same |
| Security | partial | *"Standard security already helps protect you. To feel even more confident… log in and take additional steps."* Controls are behind login. | https://web.bankofamerica.com/en/security |
| FDIC | recorded | FDIC digital sign displayed: *"FDIC-Insured - Backed by the full faith and credit of the U.S. Government"* | product page |

### Citi® Savings — Citibank, N.A. (CERT 7213) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | `citi.com/banking/savings-account` and `citi.com/banking/current-interest-rates/savings-accounts` both returned a JavaScript shell containing only a "Skip to Content" link. Citi's own disclosure text (as indexed) states APY is *"determined by Rate Region, Relationship Tier and applicable promotion"*. | https://www.citi.com/banking/savings-account |
| Product / fee / app / security | **blank** | Rate, fee and product detail pages did not render any content to a non-JavaScript fetch in this pass. Left blank rather than sourced elsewhere. | — |
| FDIC | recorded | Citibank, N.A. is an FDIC-insured institution (CERT 7213 from FDIC data) | https://banks.data.fdic.gov/bankfind-suite/bankfind/details/7213 |

### Wells Fargo Way2Save® Savings — Wells Fargo Bank, N.A. (CERT 3511) — ✅ APY verified, no date published

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **0.01%** | Table: *"Standard Interest Rate 0.01% / Annual Percentage Yield (APY) 0.01%"* for *"$0 or more"*. No effective date is shown on the page. | https://www.wellsfargo.com/savings-cds/way2save/ |
| Minimum to open | $25 | *"Open with $25"* / *"$25 minimum opening deposit"* | same |
| Monthly fee | $5 | *"$5 or $0 each fee period"* | same |
| Fee waiver | recorded | $300 minimum daily balance; 1 automatic transfer of $25+ per fee period; 1 automatic transfer of $1+ each business day; Save As You Go transfers; primary owner 24 or under | same |
| Opening rules | recorded | 18+ to apply online, 17 and under at a branch; SSN, valid ID, residential address, $25 | same |
| App | Wells Fargo Mobile® app | *"Download the Wells Fargo Mobile® app"*; in-app Security Center | https://www.wellsfargo.com/mobile-online-banking/ |
| Security | recorded | *"From zero-liability protection to 24/7 fraud monitoring"* | https://www.wellsfargo.com/privacy-security/fraud/ |

### U.S. Bank Bank Smartly® Savings — U.S. Bank N.A. (CERT 6548) — ✅ APY verified 2026-10-21

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | 0.05% standard; 1.00% / 2.00% / **3.50%** relationship tiers | *"The displayed Annual Percentage Yield (APY) and interest rates are effective as of October 21, 2026 for ZIP code"*; table: standard 0.05%; relationship tiers Under $5,000 → 1.00%; $5,000–$24,999.99 → 2.00%; $25,000+ → 3.50% | https://www.usbank.com/bank-accounts/savings-accounts/bank-smartly-savings/savings-account-interest-rates.html |
| Condition on 3.50% | recorded | *"when you are an account owner of a U.S. Bank Smartly® Checking account, Safe Debit account, or U.S. Bank Smartly™ Visa Signature® Card and a Combined Qualifying Balance (CQB) of at least $25,000"* | https://www.usbank.com/bank-accounts/savings-accounts.html |
| Minimum to open | $25 | *"Minimum opening deposit $25"* | same |
| Monthly fee | $5 | *"MONTHLY MAINTENANCE FEE $5"*; *"can be waived when you are an account owner of eligible accounts"* | same + rate page |
| App | U.S. Bank Mobile App | *"with the award-winning U.S. Bank Mobile App"* | https://www.usbank.com/online-mobile-banking/mobile-banking.html |
| Security | recorded | *"Industry's strongest available encryption and zero fraud liability"*; *"supports Touch/Face ID (iOS) and fingerprint/face scan (Android)"*; card lock/unlock | same |
| Location caveat | flagged | *"APYs may vary by location"* — the rate sheet read was ZIP 55402 | rate page |

### PNC High Yield Savings — PNC Bank, N.A. (CERT 6384) — ⚠️ APY partial

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **3.15% (partial)** | Page `<title>`: *"High Yield Savings Account | 3.15% Annual Percentage Yield APY"*. Body: *"This Product Isn't Available in Your Area"* — no rate table, no effective date. | https://www.pnc.com/en/personal-banking/banking/savings/high-yield-savings.html |
| Rate centre | no data | `deposit-rates/high-yield-savings.html` returned the same geo-block for this location | https://www.pnc.com/en/personal-banking/banking/deposit-rates/high-yield-savings.html |
| Minimum / fee | **blank** | Not disclosed on an accessible page | — |
| App | PNC Mobile Banking | App Store / Google Play badges published on PNC pages | https://www.pnc.com/en/personal-banking/banking/online-and-mobile-banking.html |
| FDIC | recorded | *"FDIC insured to the maximum permitted by law"* | PNC savings pages |

### Truist One Savings — Truist Bank (CERT 9846) — ✅ APY verified 2026-09-28

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **0.01%** at every tier | *"Interest rates and annual percentage yields (APY) are accurate as of 9/28/2026"*; every tier row ($0–$4,999.99 through $5,000,000+) shows rate 0.01% / APY 0.01% | https://www.truist.com/savings/truist-one-savings/disclosures-and-fees |
| Minimum to open | $50 | *"Minimum Opening Deposit $50"* | same |
| Monthly fee | $5 | *"Monthly Maintenance Fee $5"*, waived by $300 minimum daily ledger balance, a $25+ recurring internal transfer, any related Truist checking account, or an owner under 18 | same |
| Withdrawals | 6 free / $5 each after | *"The Withdrawal Limit Fee of $5 will be assessed per withdrawal over six (6)"* | same |
| App | recorded | *"With online and mobile banking, you'll be able to check on your savings whenever you want"* + app QR code | https://www.truist.com/savings/truist-one-savings |

### TD Signature Savings — TD Bank, N.A. (CERT 18409) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | The page's rate tables are empty in the served HTML and the page shows *"You are viewing info for ."* with no location selected; TD says rates are shown per location. | https://www.td.com/us/en/personal-banking/savings-accounts |
| Minimum to open | $0 (with 45-day rule) | *"There is no minimum opening deposit required to open the account. However, if you do not make a deposit within 45 days, your account will automatically close."* | same |
| Monthly fee | $15 | *"Monthly fee: $15"*; waived by a $10,000 minimum daily balance or a linked eligible TD Beyond/Complete checking account | same |
| App | TD Mobile Banking App | *"Download the TD Mobile Banking App… check your balances, make transfers, pay bills, deposit checks"* | https://www.td.com/us/en/personal-banking/online-banking |
| Security | recorded | *"Log in with Touch ID and single-use security code. At setup, you can select how to receive your security code: text or voice message"* | same |

### Capital One 360 Performance Savings — Capital One, N.A. (CERT 4297) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | Page states *"APY (Annual Percentage Yield) is variable and effective 10/21/2026"* but the value is rendered as **"NaN APY"** in the served HTML. | https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/ |
| Minimum / fee | $0 / $0 | *"There are no fees to open or keep your account"*; *"There's no minimum balance required to maintain your account"* | same |
| App | Capital One Mobile | *"Find the Capital One Mobile app in the App Store and Google Play"* | https://www.capitalone.com/digital/tools/mobile/ |
| Security | recorded | *"two-step authentication, real-time fraud and purchase alerts and a card lock feature"*; biometric sign-in | https://www.capitalone.com/bank/security-fraud-protection/ and the app page |
| FDIC aggregation | recorded | *"any Capital One or Discover Bank deposit accounts opened on or after May 18, 2025 are immediately counted with your other Capital One deposit accounts for determining deposit insurance coverage"* | product page |

### Citizens One Deposit Savings — Citizens Bank, N.A. (CERT 57957) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | No APY text on the savings page (rates are given in account documents / at application). | https://www.citizensbank.com/savings/savings-accounts/overview.aspx |
| Minimum to open | $0 | *"No minimum deposit to open"*; FAQ: *"You may open a Citizens savings account with any amount."* | same |
| Monthly fee | $4.99 | *"Waive the $4.99 Monthly Maintenance Fee"* with one deposit of any amount per statement period or a $200 minimum daily balance; first 4 fees waived on new accounts | same |
| Withdrawals | none | *"Citizens does not limit transactions, including withdrawals, on savings accounts."* | same |
| Footprint | 15 states + DC | *"Citizens offers personal savings accounts in the following states: CT, DC, DE, FL, MD, MA, MI, NH, NJ, NY, OH, PA, RI, VT or VA"* | same |
| App / security | recorded | *"Download the Citizens Mobile Banking App"*; *"24/7 fraud monitoring"* | same |

### Fifth Third Momentum® Savings — Fifth Third Bank, N.A. (CERT 6672) — ⛔ APY blank

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **blank** | No APY on the savings page; *"Visit a branch or call your banker for promotional rates."* | https://www.53.com/content/fifth-third/en/personal-banking/bank/savings.html |
| Minimum to open | $0 | *"Minimum opening deposit $0"* | same |
| Monthly fee | $7.50 | *"$0 if you have a Fifth Third Checking Account or have an account balance of $500 or greater. Otherwise, it is $7.50."* | same |
| App | **blank** | The digital-banking page I tried (`/personal-banking/digital-banking.html`) returned 404; the savings page does not name an app. Not recorded. | — |

### HSBC Premier Relationship Savings — HSBC Bank USA, N.A. (CERT 57890) — ✅ APY verified, no date published

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | 0.05% standard / **3.10%** relationship | *"Standard APY (minimum balance: $1) 0.05% APY"*; *"Relationship APY (minimum balance: $1) 3.10% APY"*. No effective date is shown. | https://www.us.hsbc.com/savings-accounts/products/relationship-savings/ |
| Condition on 3.10% | recorded | Relationship APY applies automatically for the rest of the month of opening + 3 months; then requires one monthly qualifying criterion ($500 debit spend, $500 card payments, $5,000 direct deposits, an HSBC-serviced mortgage, or Premier Elite status) | same |
| Opening rules | recorded | *"you must be an HSBC Premier client with a new or existing HSBC Premier checking account"*; 18+ | same |
| App | recorded | *"easily transfer money domestically and internationally with our mobile and online banking"* | same |

### Ally Savings — Ally Bank (CERT 57803) — ✅ APY verified 2026-10-21

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **3.10%** | *"Annual Percentage Yield 3.1% correct as of 10/21/26"*; *"Our Annual Percentage Yields (APYs) are accurate as of 10/21/2026."* | https://www.ally.com/bank/savings-account-rates/ |
| Minimum | $0 | *"No minimum balance required to open an account or earn APY."* | same |
| Fees | $0 | *"No monthly maintenance fees"* | same |
| Withdrawal limit | 10 per cycle | *"We limit certain types of withdrawals and transfers from Savings and Money Market Accounts to a combined total of 10 per statement cycle."* | same |
| Trust accounts | yes | *"Available to open in the name of a Trust."* | same |
| Security | recorded | *"guarantees that you will not be liable for any unauthorized Online or Mobile Banking transaction as long as you report the unauthorized transaction… within 60 days"*; *"multi-factor authentication"* | https://www.ally.com/security/ |

### American Express High Yield Savings — American Express National Bank (CERT 27471) — ✅ APY verified 2026-10-21

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **3.20%** | *"The Annual Percentage Yield (APY) as advertised is accurate as of 10/21/2026"*; card: *"High Yield Savings (HYSA) 3.20% APY"* | https://www.americanexpress.com/en-us/banking/online-savings/account/ |
| Minimum / fee | $0 / $0 | *"There is no minimum balance required to open your Account, to avoid being charged a fee, or to obtain the Annual Percentage Yield (APY) disclosed to you"* | same |
| FDIC | recorded | *"Each depositor is insured to at least $250,000 per depositor, per insured bank, per ownership category."* | same |
| App | Amex App | *"Manage your High Yield Savings Account 24/7 with the Amex® App"* | https://www.americanexpress.com/en-us/support/digital/amex-mobile-app/ |
| Security | recorded | *"Two-step verification"*; passkeys; biometrics; *"SafeKey"*; Voice ID; device management | https://www.americanexpress.com/en-us/security/ |

### Marcus Online Savings — Goldman Sachs Bank USA (CERT 33124) — ✅ APY verified 2026-10-21

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | **3.50%** | *"Annual percentage yield as of October 21, 2026. APY may change at any time before or after account is opened."* | https://www.marcus.com/us/en/savings/high-yield-savings |
| Minimum / fee | $0 / $0 | *"No fees. No minimum deposit."*; *"We don't require a minimum deposit or a credit check."* | same |
| Withdrawals | no limit | *"At this time, there is no limit to the number of withdrawals or transfers you can make from your Online Savings Account."* | same |
| Referral promo | +1.00% for 3 months | *"you both could earn an extra 1.00% APY for 3 months"*; *"If one referral is made in a year… combined APY of 3.75%"*; up to 5 referrals | https://www.marcus.com/us/en/savings/referrals |
| App | Marcus app | *"Complete the application and open your account online or in the Marcus app"* | savings page |
| FDIC | recorded | Goldman Sachs Bank USA, Member FDIC (site-wide disclosure) | https://www.marcus.com/ |

### SoFi Savings — SoFi Bank, N.A. (CERT 26881) — ✅ APY verified 2026-10-20

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | 3.30% standard; 4.40% with boost | *"Get a 1.10% boost on our savings APY of 3.30% … (added to the 3.30% as of 10/20/26) for up to 6 months"* | https://www.sofi.com/banking/high-yield-savings-account/ |
| Conditions | recorded | open by 12/31/27 and set up eligible direct deposit within 60 days (or $5,000 qualifying deposits every 31 days) | same |
| Minimum / fee | $0 / $0 | *"Zero account fees… no monthly fees, overdraft fees, or minimum balance fees"*; *"Minimum deposit to open $0"* in SoFi's own comparison table | same |
| Bonus | $50 or $400 | *"Earn a $50 or $400 cash bonus with eligible direct deposit… of $1,000 or more"* | same |
| FDIC | recorded, flagged | *"Access additional FDIC-insurance up to $3M through a network of participating banks"* — bank marketing claim, flagged on the site | same |
| App | SoFi app | *"Deposit checks anytime, anywhere, right from the SoFi app"* | same |

### Barclays Tiered Savings — Barclays Bank Delaware (CERT 57203) — ✅ APY verified 2026-10-07

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | 3.50% (< $250k); **3.65%** ($250k–$1M) | Tier table: *"$250,000 to $1,000,000 → 3.65%"*, *"Less than $10,000 → 3.50%"* and intermediate tiers 3.50%; *"This information is accurate as of 10/07/2026."* | https://banking.us.barclays/tiered-savings.html |
| Minimum / fee | $0 / $0 | *"No monthly maintenance fees. No minimum balance to open."* | same |
| Limits | $1M per account, max 3 accounts | FAQ: *"you can only deposit a maximum of $1 million per Tiered Savings account"*; *"each customer can only have a maximum of 3 open Tiered Savings accounts"* | same |
| Bonus | $200 | *"open an account through 10/31/2026, fund your new Barclays Tiered Savings account with at least $25,000 within the first 30 days… and maintain the balance of at least $25,000 for 120 consecutive days"*; bonus ~60 days later; 1099-INT | same + https://banking.us.barclays/ |

### CIT Bank Platinum Savings — First-Citizens Bank & Trust Company, CIT Bank division (CERT 11063) — ✅ APY verified 2026-07-01

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| APY | 0.25% (< $5k); **3.75%** (≥ $5k) | *"APYs — Annual Percentage Yields are accurate as of July 1, 2026: 0.25% APY on balances of $0.01 to $4,999.99; 3.75% APY on balances of $5,000.00 or more."* | https://www.cit.com/cit-bank/platinum-savings |
| Minimum to open | $100 | *"The minimum to open a Platinum Savings account is $100."* | same |
| Fees | $0 | *"No account opening or monthly service fees"* | same |
| Boost | 4.25% for 6 months | *"Enter promo code BOOST50 to receive a 0.50% APY bonus for six months from account opening"*; promotion *"begins on September 29, 2026, and ends December 15, 2026"* | https://www.cit.com/cit-bank/platinum-savings/boost |
| App | CIT Bank mobile app | *"CIT Bank's mobile app makes it easy to manage your account."* | product page |
| FDIC aggregation | recorded | *"Deposits held under the names of First-Citizens Bank and Trust Company and all banks which are a division of FCB are not separately insured."* | product page |

### Discover Online Savings — Discover Bank (CERT 5649) — ⛔ inactive / merged

| Field | Value recorded | Evidence | URL |
| --- | --- | --- | --- |
| Institution status | inactive | FDIC API returns `"ACTIVE": 0` for CERT 5649 (Discover Bank). | https://api.fdic.gov/banks/institutions?filters=CERT%3A5649 |
| FDIC aggregation | recorded | Capital One: accounts opened on/after 2025-05-18 *"are immediately counted with your other Capital One deposit accounts"* | Capital One product page |

---

## 3. FDIC insurance rules

| Rule | Value used | Exact FDIC wording | URL |
| --- | --- | --- | --- |
| Standard coverage | $250,000 | *"Your deposits are automatically insured to at least $250,000 at each FDIC-insured bank."* | https://www.fdic.gov/resources/deposit-insurance/ |
| Per ownership category | $250,000 | *"FDIC deposit insurance covers $250,000 per depositor, per FDIC-insured bank, for each account ownership category."* | https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance |
| Aggregation | — | *"All of your deposits in the same ownership category in the same FDIC-insured bank are added together for the purpose of determining FDIC deposit insurance coverage."* | same |
| Joint accounts | $250,000 per co-owner | *"you will be insured… up to $250,000 for all of your joint ownership account deposits"* (per owner) | same |
| Trust accounts | $250,000 per beneficiary, cap $1,250,000 | *"An owner's trust deposits are insured for up to $250,000 per eligible beneficiary, up to a maximum of $1,250,000 if five or more eligible beneficiaries are named."* | https://www.fdic.gov/financial-institution-employees-guide-deposit-insurance/trust-accounts |
| Trust rule effective date | 2024-04-01 | *"As of April 1, 2024, the maximum insurance coverage for a trust owner with five or more beneficiaries is $1,250,000 per owner for all trust accounts…"* | https://www.fdic.gov/resources/deposit-insurance/brochures/insured-deposits |
| Calculator | EDIE | *"EDIE lets consumers and bankers know, on a per-bank basis, how the insurance rules and limits apply…"* | https://edie.fdic.gov/ |

## 4. Benchmarks

| Benchmark | Value used | Evidence | URL |
| --- | --- | --- | --- |
| FDIC national savings rate | **0.38%** | Table "National Deposit Rates": Savings = 0.38; page header *"National Rates and Rate Caps – October 2026"*, *"Revised Rule October 19, 2026"*; *"Monthly Rate Cap Information as of October 19, 2026"*. Footnote: savings rates are based on the $2,500 product tier. | https://www.fdic.gov/national-rates-and-rate-caps |
| 1-year Treasury | 4.54% | same table, "Treasury Yield" column at 12 month CD tenor | same |
| 2-year Treasury | 4.88% | same, 24 month | same |
| 3-year Treasury | 5.00% | same, 36 month | same |
| 5-year Treasury | 5.09% | same, 60 month | same |

## 5. URLs that failed or behaved oddly during verification

| URL | Result | Consequence |
| --- | --- | --- |
| `chase.com/.../interest-rates?zipCode=10001` | No rate table served | Chase APY blank, flagged |
| `bankofamerica.com/deposits/savings/savings-accounts/rates/` | 404 | BofA APY blank, flagged |
| `bankofamerica.com/deposits/savings/savings-accounts/` | `$XXXX` placeholders | BofA fee blank, flagged |
| `capitalone.com/bank/savings-accounts/rates/` | 404 ("page not found") | Capital One APY blank, flagged |
| `capitalone.com/.../online-performance-savings-account/` | APY renders as `NaN` | Capital One APY blank, flagged |
| `citi.com/banking/savings-account`, `citi.com/banking/current-interest-rates/savings-accounts` | JavaScript-only shell | Citi APY blank, flagged |
| `pnc.com/.../high-yield-savings.html` | "This Product Isn't Available in Your Area" | PNC 3.15% marked partial |
| `td.com/us/en/personal-banking/savings-accounts` | empty rate tables, no location | TD APY blank, flagged |
| `truist.com/bank/checking-savings/savings-accounts`, `truist.com/savings/interest-rates` | 404 (wrong paths) | rate found on the disclosure page instead |
| `synchronybank.com/banking/savings/`, `synchrony.com/banking/savings-account` | 404 | Synchrony dropped from the study rather than guessed |
| `usbank.com/bank-accounts/savings-accounts/standard-savings.html` | 404 | used the savings-accounts index and rate sheet |
| `pnc.com/.../savings/high-yield-savings-account.html` | 404 | used `high-yield-savings.html` |
| `53.com/.../digital-banking.html` | 404 | Fifth Third app left blank |
| `schwab.com/high-yield-investor-savings`, `schwab.com/banking/savings` | 404 | Schwab dropped rather than guessed |
| `marcus.com/us/en/security`, `marcus.com/us/en/mobile-app`, `sofi.com/security/`, `sofi.com/banking/mobile-app/` | 404 | security/app facts taken from the product pages instead |
| `ally.com/mobile-banking/`, `ally.com/bank/mobile-banking/` | 404 | app fact taken from Ally's security page, which covers "Online or Mobile Banking" |
| `barclaysus.com/online-savings.html` | redirected to `banking.us.barclays` | recorded the canonical domain |
| `home.treasury.gov` daily yield CSV | HTTP 500 | Treasury yields taken from the FDIC table instead |
| `fdic.gov/resources/deposit-insurance/financial-products-insured/revocable-trusts` | 404 | used the Trust Accounts section of the FDIC employee guide |

## 6. Arithmetic checks

Spot-checked by hand against the generated `data/analysis.json`:

- $250,000 × 3.75% = **$9,375.00** (CIT) — matches `by_size["250000"]`.
- $250,000 × 3.65% = **$9,125.00** (Barclays ≥ $250k) — matches.
- $250,000 × 0.01% = **$25.00** (Truist / Wells Fargo) — matches.
- $1,000,000 blended at (3.75 + 3.65 + 3.50 + 3.50)/4 = **3.60%** → $36,000 year-one interest — matches the FDIC plan table.
- SoFi promo year one: $250,000 × 4.40% for 6 months ($5,440.80), then 3.30% on the higher balance for 6 months ($4,180.56) = **$9,621.36** — matches the promotion table.
- $1,250,000 × 3.75% = **$46,875.00** (trust structure) — matches.
- CIT boost year one: $250,000 × 4.25% for 6 months ($5,257.22), then 3.75% for 6 months ($4,742.03) = **$9,999.25** — matches.

## 7. Repository and site checks

- `python3 build.py` → 8 pages generated; validation gate: **0 errors** (3 warnings, each a known documentation gap: two banks publish a verified rate with no effective date; one inactive entity has no product page).
- `python3 check_links.py` → all local links resolve; external URLs are unreachable from this sandbox's shell egress, so each source URL was instead opened and read individually during research (see above).
- JSON schema gate in `build.py`: refuses to build if a product marked `verified` has no tier value or no source link.
