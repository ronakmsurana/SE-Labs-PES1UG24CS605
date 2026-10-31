import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ==========================================
# Tests for annual_premium
# ==========================================

def test_annual_premium_invalid_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_annual_premium_driver_too_young():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_annual_premium_young_driver_with_anti_theft():
    # Hatchback base: 8000, Age < 25 (+4000) = 12000
    # Claims == 0 (-2400) = 9600, Anti-theft (-500) = 9100
    assert annual_premium("hatchback", 20, 0, True) == 9100


def test_annual_premium_senior_driver_multiple_claims():
    # SUV base: 15000, Age >= 60 (+2000) = 17000
    # Claims > 2 (* 2) = 34000, Anti-theft False = 34000
    assert annual_premium("suv", 65, 3, False) == 34000


def test_annual_premium_standard_driver():
    # Sedan base: 12000, Age in [25, 59], Claims in [1, 2]
    assert annual_premium("sedan", 35, 1, False) == 12000


# ==========================================
# Tests for no_claim_bonus
# ==========================================

def test_no_claim_bonus_negative_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_no_claim_bonus_tiers():
    assert no_claim_bonus(5) == 50
    assert no_claim_bonus(3) == 35
    assert no_claim_bonus(1) == 20
    assert no_claim_bonus(0) == 0


# ==========================================
# Tests for claim_payout
# ==========================================

def test_claim_payout_invalid_amounts():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 5000, 500, False)
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(1000, 5000, -100, False)


def test_claim_payout_total_loss():
    assert claim_payout(2000, 10000, 500, True) == 10000


def test_claim_payout_damage_under_deductible():
    assert claim_payout(400, 10000, 500, False) == 0


def test_claim_payout_exceeds_insured_value():
    assert claim_payout(15000, 10000, 1000, False) == 10000


def test_claim_payout_standard():
    assert claim_payout(5000, 10000, 1000, False) == 4000

