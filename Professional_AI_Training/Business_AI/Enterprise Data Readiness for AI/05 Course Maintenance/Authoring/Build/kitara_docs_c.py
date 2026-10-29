"""Kitara document corpus, part C: 30 claims and complaint letters with fictional personal data (one page each)."""
import numpy as np
from kitara_docs_a import doc
from kitara_names import (phone, national_id, full_name, fmt_ugx, PLACES_UG, DISTRICTS_UG)

TYPES = ["motor"] * 6 + ["home"] * 4 + ["life"] * 3 + ["approve"] * 4 + ["repud"] * 3 + ["wallet"] * 4 + ["loan"] * 3 + ["slow"] * 3
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September"]
VEH = ["Toyota Premio", "Toyota Corolla", "Subaru Forester", "Nissan Note", "Mazda Demio", "Toyota Hilux", "Honda Fit", "Toyota Noah"]
LETTER_FACTS = []


def _date(g, lo=1, hi=9):
    m = int(g.integers(lo, hi + 1))
    d = int(g.integers(2, 27))
    return f"{d} {MONTHS[m - 1]} 2026", f"2026-{m:02d}-{d:02d}"


def build_letters(seed=7731):
    LETTER_FACTS.clear()
    g = np.random.default_rng(seed)
    for i, t in enumerate(TYPES, start=1):
        is_life0 = (t == "life" and sum(1 for x in TYPES[:i - 1] if x == "life") == 0)
        name, fem = full_name(g, female=True if is_life0 else None)
        title = ("Mrs" if is_life0 else "Ms" if fem else "Mr")
        cid = f"KT-{g.integers(1000000, 9999999)}"
        nid = national_id(g)
        ph = phone(g)
        ref = f"CL-2026-{g.integers(300, 990):04d}"
        dtxt, diso = _date(g)
        town = PLACES_UG[g.integers(0, len(PLACES_UG))]
        amt = int(np.round(g.uniform(1.2, 38) * 1e6 / 50000) * 50000)
        pol = f"MP-2025-{g.integers(10000, 99999)}"
        veh = VEH[g.integers(0, len(VEH))]
        reg = f"U{'ABCDEFGHJKLMNP'[g.integers(0, 14)]}{'ABCDEFGHJKLMNP'[g.integers(0, 14)]} {g.integers(100, 999)}{'ABCDEFGHJKLMNP'[g.integers(0, 14)]}"
        head = f"{title} {name}\n{town}, Uganda\nPhone: {ph}\n\n{dtxt}\n\n"
        sens, groups, personal, fam = "restricted", "claims", "Y", "claims_letter"
        fact = dict(tag=f"L{i:02d}", type=t, name=name, cust_id=cid, nid=nid, phone=ph, ref=ref, amount=amt, date=dtxt, town=town)
        if t == "motor":
            body = head + f"""The Claims Manager
Kitara Assurance, Kampala

Dear Sir or Madam,

NOTIFICATION OF MOTOR CLAIM {ref}, POLICY {pol}

I am writing to report an accident involving my {veh}, registration {reg}. The accident happened on {dtxt.split(' ', 1)[0]} {dtxt.split(' ', 1)[1]} near {town}. A lorry reversed into the front of my car while it was parked outside my shop. Nobody was hurt. I reported the matter to the police the same day.

The garage has estimated the repair at {fmt_ugx(amt)}. I attach the police report, my driving permit and photographs. My customer number is {cid} and my national identity number is {nid}.

Please tell me what else you need. I can be reached on {ph}.

Yours faithfully,
{name}"""
            fact["note"] = f"motor claim for {veh}"
        elif t == "home":
            ev = ["a fire in the kitchen", "a burglary while we were at church", "flooding after heavy rain", "a storm that removed part of the roof"][i % 4]
            body = head + f"""The Claims Manager
Kitara Assurance, Kampala

Dear Sir or Madam,

HOME INSURANCE CLAIM {ref}

My house at {town} was damaged by {ev} on {dtxt}. I hold a home insurance policy with you. My customer number is {cid} and my national identity number is {nid}.

The loss is as follows: the damage to the building is estimated at {fmt_ugx(amt * 0.7)} and the household contents lost are estimated at {fmt_ugx(amt * 0.3)}, a total of {fmt_ugx(amt)}. I have attached an inventory and photographs. A neighbour, a Local Council chairperson, can confirm the loss.

Please send an assessor. You can call me on {ph}.

Yours faithfully,
{name}"""
            fact["amount"] = amt
        elif t == "life":
            k = [j for j in range(i - 1) if TYPES[j] == "life"].__len__()
            if k == 0:
                cause = "My husband died on {d} after a long illness. He had kidney failure and had been on dialysis twice a week since 2024. The doctor's report is attached."
                sens, groups = "confidential", "claims"
                fact["health"] = "kidney failure and dialysis"
            elif k == 1:
                cause = "My brother died on {d} in a road accident on the Masaka road. The police report and the death certificate are attached."
            else:
                cause = "My father died on {d} at home in his sleep. The doctor certified the cause as a heart attack. The death certificate is attached."
            death, _ = _date(g, 1, 5)
            dd = int(g.integers(3, 27))
            dtxt, diso = f"{dd} July 2026", f"2026-07-{dd:02d}"
            head = f"{title} {name}\n{town}, Uganda\nPhone: {ph}\n\n{dtxt}\n\n"
            fact["date"] = dtxt
            body = head + f"""The Life Claims Section
Kitara Assurance, Kampala

Dear Sir or Madam,

LIFE INSURANCE CLAIM {ref}

I am the named beneficiary of the life policy of the late {'Henry' if k == 0 else 'Peter' if k == 1 else 'Samuel'} {name.split()[1]}, policy LP-2024-{g.integers(10000, 99999)}, cover {fmt_ugx(amt * 5)}. """ + cause.format(d=death) + f"""

I am attaching the death certificate, the policy document and my identity card (national ID {nid}). My customer number is {cid}. Please tell me how long the claim will take. I can be reached on {ph}.

Yours faithfully,
{name}"""
            fact["amount"] = amt * 5
        elif t == "approve":
            days = int(g.integers(14, 29))
            body = f"""KITARA ASSURANCE LIMITED
Claims Department, Kampala

{dtxt}
Ref: {ref}

{title} {name}
{town}
Customer ID: {cid}

Dear {title} {name.split()[1]},

SETTLEMENT OF CLAIM {ref}

We have completed the assessment of your claim under policy {pol}. The claim is accepted. We will pay {fmt_ugx(amt)}, after the excess, directly to your account with Kitara Bank. The payment will be made within {days} days of the date of this letter, which is inside our commitment of 30 days.

If you have a question please call the Claims Officer on 0800 100 200 and quote the reference above.

Yours faithfully,
Claims Officer
Kitara Assurance"""
            fact["days"] = days
        elif t == "repud":
            reason = ["the policy had lapsed on 30 June 2026 because the premium was not paid within the 30 days grace period",
                      "the driver did not hold a valid driving permit at the time of the accident, which is excluded under the policy",
                      "the claim is for loss that happened before the policy started"][len([j for j in range(i - 1) if TYPES[j] == "repud"])]
            body = f"""KITARA ASSURANCE LIMITED
Claims Department, Kampala

{dtxt}
Ref: {ref}

{title} {name}
{town}
Customer ID: {cid}, phone {ph}

Dear {title} {name.split()[1]},

DECISION ON CLAIM {ref}

We have reviewed your claim of {fmt_ugx(amt)}. We regret that we cannot pay it, because {reason}. This decision follows the terms of your policy and the Claims Handling SOP.

If you disagree you may write to the Head of Customer Service within 30 days. If we have not settled your complaint after 30 days you may take the matter to the insurance regulator.

Yours faithfully,
Senior Claims Officer
Kitara Assurance"""
            fact["decision"] = "declined"
        elif t == "wallet":
            body = head + f"""The Customer Service Manager
Kitara Bank

Dear Sir or Madam,

COMPLAINT: DOUBLE DEDUCTION ON MY MOBILE WALLET, REF {ref}

On {dtxt} I sent {fmt_ugx(amt / 10)} from my Kitara Mobile Wallet to pay a school bill. The money was deducted twice from my wallet but the school received it once. The agent at {town} told me the message was sent two times by the system and that I should wait. I have waited for two weeks.

Please refund {fmt_ugx(amt / 10)}. My wallet number is {ph} and my customer number is {cid}. My national identity number is {nid}.

Yours faithfully,
{name}"""
            fact["amount"] = int(amt / 10)
        elif t == "loan":
            body = head + f"""The Branch Manager
Kitara Bank, {town} Branch

Dear Sir or Madam,

COMPLAINT ABOUT MY LOAN STATEMENT, REF {ref}

I took a business loan of {fmt_ugx(amt * 2)} on {dtxt}. My statement shows a balance of {fmt_ugx(amt * 2 + 600000)} even though I have paid every instalment on time and I attach the receipts. I think interest has been charged twice in one month.

My customer number is {cid} and my national identity number is {nid}. Please correct the statement and write to me. My phone is {ph}.

Yours faithfully,
{name}"""
            fact["amount"] = amt * 2
        else:  # slow
            body = head + f"""The Head of Customer Service
Kitara Assurance, Kampala

Dear Sir or Madam,

COMPLAINT ABOUT DELAY IN MY CLAIM {ref}

I submitted my motor claim on {dtxt} and sent the last document one month later. Nobody has called me since, and my {veh} is still at the garage, which now charges me UGX 20,000 a day for parking. The garage estimate is {fmt_ugx(amt)}.

My customer number is {cid}. Your charter promises to settle claims within 30 days. Please tell me when I will be paid. My phone is {ph}.

Yours faithfully,
{name}"""
        LETTER_FACTS.append(fact)
        gp = "claims;legal_compliance" if t in ("wallet", "loan", "slow") else groups
        doc(f"L{i:02d}", f"claims letters/Letter {i:02d} {ref} {name.split()[1]}.pdf", f"{'Complaint' if t in ('wallet','loan','slow') else 'Claim letter'} {ref} ({t})",
            fam, "1", "current", diso, "Claims" if t not in ("wallet", "loan") else "Customer Service", sens, gp, body, personal=personal, hf=False)
