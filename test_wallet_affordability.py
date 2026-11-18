import pytest
from wallet_affordability import can_afford


class TestWalletAffordability:
    # 1. Valid Purchases & Return Type Verification
    def test_afford_greater_balance(self):
        """Catches bug in wallet_affordability.py where int(...) returns 1 instead of True."""
        result = can_afford(1000, 500)
        assert result is True
        assert type(result) is bool

    def test_afford_exact_balance(self):
        result = can_afford(500, 500)
        assert result is True
        assert type(result) is bool

    def test_afford_zero_price_zero_balance(self):
        result = can_afford(0, 0)
        assert result is True
        assert type(result) is bool

    def test_afford_zero_price_positive_balance(self):
        result = can_afford(250, 0)
        assert result is True
        assert type(result) is bool

    # 2. Insufficient Funds (False & bool type)
    def test_afford_insufficient_funds(self):
        """Catches bug returning int 0 instead of False."""
        result = can_afford(499, 500)
        assert result is False
        assert type(result) is bool

    def test_afford_zero_balance_positive_price(self):
        result = can_afford(0, 50)
        assert result is False
        assert type(result) is bool

    # 3. Value Boundaries & Range Violations (ValueError)
    def test_afford_negative_balance(self):
        with pytest.raises(ValueError):
            can_afford(-1, 100)

    def test_afford_negative_price(self):
        with pytest.raises(ValueError):
            can_afford(100, -50)

    # 4. Type Enforcement (TypeError)
    @pytest.mark.parametrize(
        "bal, price",
        [
            (True, 100),
            (100, False),
            (25.5, 10),
            (100, 10.0),
            ("500", 100),
            (500, "100"),
            (None, 50),
            (100, None),
        ],
    )
    def test_afford_invalid_types(self, bal, price):
        with pytest.raises(TypeError):
            can_afford(bal, price)