"""Fictional name, place and number pools. Combinations are random; any match with a real person is chance."""
import numpy as np

GIVEN_F = ["Ruth", "Grace", "Sarah", "Esther", "Joan", "Agnes", "Rebecca", "Mary", "Juliet", "Florence", "Betty", "Prossy", "Harriet", "Doreen",
           "Winnie", "Sylvia", "Irene", "Racheal", "Caroline", "Aisha", "Zainab", "Stella", "Lillian", "Josephine", "Immaculate", "Scovia", "Mercy",
           "Faith", "Eunice", "Wanjiku", "Achieng", "Njeri", "Wambui", "Chebet", "Mwikali", "Namusoke", "Nakato", "Babirye", "Atim", "Akello"]
GIVEN_M = ["Moses", "Brian", "Joseph", "David", "Peter", "Patrick", "Isaac", "Samuel", "Henry", "Daniel", "Emmanuel", "Francis", "Ronald", "Allan",
           "Denis", "Robert", "Charles", "Tonny", "Geoffrey", "Hassan", "Ibrahim", "Julius", "Kenneth", "Andrew", "Fred", "Wilson", "Stephen",
           "Nelson", "Martin", "Otieno", "Kamau", "Mutua", "Odhiambo", "Kimani", "Opio", "Okello", "Mugisha", "Wasswa", "Kato", "Mukasa"]
FAMILY = ["Nankya", "Kasozi", "Ssemwogerere", "Okello", "Mugisha", "Tumusiime", "Namutebi", "Ochieng", "Wafula", "Byaruhanga", "Atim", "Opio", "Nakato",
          "Kiiza", "Mwesigwa", "Akello", "Ssebunya", "Lubega", "Namukasa", "Kato", "Mukasa", "Nabirye", "Kigozi", "Muhumuza", "Tusiime", "Kyomuhendo",
          "Aryampa", "Auma", "Odongo", "Mutesi", "Ssali", "Nalubega", "Kamya", "Waiswa", "Kisakye", "Bukenya", "Kabuye", "Namatovu", "Rukundo",
          "Ssekandi", "Mwangi", "Njoroge", "Kimani", "Wambui", "Odhiambo", "Chebet", "Mutiso", "Barasa", "Wekesa", "Kyalo", "Nsubuga", "Tendo",
          "Nabukenya", "Ahimbisibwe", "Twinomujuni", "Oryem", "Lakot", "Ojok", "Nantongo", "Birungi"]
DISTRICTS_UG = ["Kampala", "Wakiso", "Mukono", "Jinja", "Mbarara", "Gulu", "Mbale", "Masaka", "Lira", "Arua", "Kabale", "Hoima", "Soroti", "Fort Portal"]
PLACES_UG = ["Ntinda", "Kawempe", "Nansana", "Kira", "Najjera", "Entebbe Road", "Bugolobi", "Mengo", "Kyambogo", "Bweyogerere", "Mpigi", "Iganga", "Tororo"]


def phone(g, kenya=False):
    """Fictional number in a block we treat as reserved for this course: +256 700 0xx xxx or +254 700 0xx xxx."""
    return f"+{'254' if kenya else '256'} 700 0{g.integers(0, 100):02d} {g.integers(0, 1000):03d}"


def national_id(g):
    return "KX" + "".join(str(d) for d in g.integers(0, 10, 12))


def full_name(g, female=None):
    f = g.random() < 0.5 if female is None else female
    given = GIVEN_F if f else GIVEN_M
    return f"{given[g.integers(0, len(given))]} {FAMILY[g.integers(0, len(FAMILY))]}", f


def fmt_ugx(n):
    return f"UGX {int(n):,}"
