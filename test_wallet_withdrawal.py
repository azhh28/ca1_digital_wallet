import pytest
from wallet_withdrawal import withdraw


class TestWalletWithdrawal:
    # 1. Valid Transactions
    def test_withdraw_standard(self):
        assert withdraw(1000, 300) == 700

    def test_withdraw_minimum_amount(self):
        assert withdraw(100, 1) == 99

    def test_withdraw_exact_balance(self):
        """Catches bug in wallet_withdrawal.py where amount_cents >= balance_cents raises ValueError."""
        assert withdraw(500, 500) == 0

    # 2. Value Boundaries & Range Violations (ValueError)
    def test_withdraw_exceeds_balance(self):
        with pytest.raises(ValueError):
            withdraw(500, 501)

    def test_withdraw_zero_amount(self):
        with pytest.raises(ValueError):
            withdraw(500, 0)

    def test_withdraw_negative_amount(self):
        with pytest.raises(ValueError):
            withdraw(500, -10)

    def test_withdraw_negative_balance(self):
        with pytest.raises(ValueError):
            withdraw(-100, 50)

    def test_withdraw_zero_balance_zero_amount(self):
        with pytest.raises(ValueError):
            withdraw(0, 0)

    # 3. Type Enforcement (TypeError)
    @pytest.mark.parametrize(
        "bal, amt",
        [
            (True, 100),  # Booleans are explicitly rejected
            (100, False),
            (50.5, 20),
            (100, 10.0),
            ("500", 100),
            (500, "100"),
            (None, 50),
            (100, None),
            ([], 10),
        ],
    )
    def test_withdraw_invalid_types(self, bal, amt):
        with pytest.raises(TypeError):
            withdraw(bal, amt)