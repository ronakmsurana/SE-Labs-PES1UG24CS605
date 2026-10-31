import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# =====================================================================
# Branch Coverage Tests for annual_premium
# Evaluates every decision branch (True/False, boundaries, each car type)
# =====================================================================

def test_annual_premium_invalid_car_type_branch():
    """Branch: if car_type not in BASE_PREMIUM -> True"""
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_annual_premium_driver_age_under_18_branch():
    """Branch: if driver_age < 18 -> True"""
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_annual_premium_age_under_25_zero_claims_anti_theft():
    """
    Branches:
    - driver_age < 25 -> True (+4000)
    - claims_last_3_years == 0 -> True (-20%)
    - has_anti_theft -> True (-500)
    Hatchback base: 8000 + 4000 = 12000.
    Claims 0: 12000 - 2400 = 9600.
    Anti-theft: 9600 - 500 = 9100.
    """
    assert annual_premium("hatchback", 24, 0, True) == 9100


def test_annual_premium_senior_driver_high_claims_no_anti_theft():
    """
    Branches:
    - driver_age < 25 -> False, driver_age >= 60 -> True (+2000)
    - claims_last_3_years == 0 -> False, claims_last_3_years > 2 -> True (* 2)
    - has_anti_theft -> False
    SUV base: 15000 + 2000 = 17000.
    Claims > 2: 17000 * 2 = 34000.
    """
    assert annual_premium("suv", 60, 3, False) == 34000


def test_annual_premium_middle_aged_driver_moderate_claims():
    """
    Branches:
    - driver_age < 25 -> False, driver_age >= 60 -> False (neither age surcharge)
    - claims == 0 -> False, claims > 2 -> False (e.g. 1 or 2 claims, no adjustment)
    - has_anti_theft -> False
    Sedan base: 12000
    """
    assert annual_premium("sedan", 35, 1, False) == 12000
    assert annual_premium("sedan", 40, 2, False) == 12000


# =====================================================================
# Branch Coverage Tests for no_claim_bonus
# Evaluates boundary decisions: <0, >=5, >=3, >=1, <1
# =====================================================================

def test_no_claim_bonus_negative_years_branch():
    """Branch: claim_free_years < 0 -> True"""
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_no_claim_bonus_tier_5_or_more():
    """Branch: claim_free_years >= 5 -> True (returns 50)"""
    assert no_claim_bonus(5) == 50
    assert no_claim_bonus(8) == 50


def test_no_claim_bonus_tier_3_to_4():
    """Branch: >= 5 False, >= 3 True (returns 35)"""
    assert no_claim_bonus(3) == 35
    assert no_claim_bonus(4) == 35


def test_no_claim_bonus_tier_1_to_2():
    """Branch: >= 3 False, >= 1 True (returns 20)"""
    assert no_claim_bonus(1) == 20
    assert no_claim_bonus(2) == 20


def test_no_claim_bonus_zero_years():
    """Branch: >= 1 False (returns 0)"""
    assert no_claim_bonus(0) == 0


# =====================================================================
# Branch Coverage Tests for claim_payout
# Evaluates:
# - Compound condition: damage_cost < 0 OR deductible < 0 (both sub-branches)
# - is_total_loss: True / False
# - damage_cost <= deductible: True / False
# - payout > insured_value: True / False
# =====================================================================

def test_claim_payout_negative_damage_cost():
    """Branch: damage_cost < 0 (first condition of OR is True)"""
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-50, 5000, 500, False)


def test_claim_payout_negative_deductible():
    """Branch: damage_cost >= 0, deductible < 0 (second condition of OR is True)"""
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(1000, 5000, -50, False)


def test_claim_payout_total_loss_branch():
    """Branch: is_total_loss -> True (returns insured_value directly)"""
    assert claim_payout(1000, 20000, 500, True) == 20000


def test_claim_payout_damage_less_than_or_equal_to_deductible():
    """Branch: damage_cost <= deductible -> True (returns 0)"""
    assert claim_payout(300, 10000, 500, False) == 0
    assert claim_payout(500, 10000, 500, False) == 0  # Boundary check: equal


def test_claim_payout_capped_at_insured_value_branch():
    """Branch: payout > insured_value -> True (returns insured_value)"""
    # damage 12000 - deductible 1000 = 11000 > insured_value 10000
    assert claim_payout(12000, 10000, 1000, False) == 10000


def test_claim_payout_normal_payout_branch():
    """
    Branch: payout > insured_value -> False (returns payout)
    Also covers payout == insured_value boundary.
    """
    # damage 6000 - deductible 1000 = 5000 < insured_value 10000
    assert claim_payout(6000, 10000, 1000, False) == 5000
    # damage 11000 - deductible 1000 = 10000 == insured_value 10000
    assert claim_payout(11000, 10000, 1000, False) == 10000

