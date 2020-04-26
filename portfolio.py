"""
trading-server is a multi-asset, multi-strategy, event-driven execution
and backtesting platform (OEMS) for trading common markets.

Copyright (C) 2020  Sam Breznikar <sam@sdbgroup.io>

Licensed under GNU General Public License 3.0 or later.

Some rights reserved. See LICENSE.md, AUTHORS.md.
"""

from trade_types import SingleInstrumentTrade, Order, Position
from event_types import OrderEvent, FillEvent
import time


class Portfolio:
    """
    Portfolio manages the net holdings for all models, issuing order events
    and reacting to fill events to open and close positions and strategies
    dictate.

    Capital allocations to strategies and risk parameters defined here.
    """

    MAX_SIMULTANEOUS_POSITIONS = 20
    MAX_CORRELATED_TRADES = 1
    MAX_ACCEPTED_DRAWDOWN = 15          # Percentage as integer.
    RISK_PER_TRADE = 1                  # Percentage as integer OR 'KELLY'
    DEFAULT_STOP = 3                    # % stop distance if none provided.

    def __init__(self, exchanges, logger, db_other, db_client, models):
        self.exchanges = {i.get_name(): i for i in exchanges}
        self.logger = logger
        self.db_other = db_other
        self.db_client = db_client
        self.models = models

        self.pf = self.load_portfolio()

    def update_price(self, events, event):
        """
        Check price and time updates gainst existing positions.

        Args:
            events: event queue object.
            event: new market event.

        Returns:
           None.

        Raises:
            None.
        """
        pass

    def new_signal(self, events, event):
        """
        Process incoming signal event and adjust postiions accordingly.

        Args:
            events: event queue object.
            event: new market event.

        Returns:
           None.

        Raises:
            None.
        """

        if self.within_risk_limits(event):
            pass

    def new_fill(self, events, event):
        """
        Process incoming fill event and update position records accordingly.

        Args:
            events: event queue object.
            event: new market event.

        Returns:
           None.

        Raises:
            None.
        """
        pass

    def load_portfolio(self, ID=0):
        """
        Load portfolio matching ID from database or return empty portfolio.
        """

        portfolio = self.db_other['portfolio'].find_one({"id": ID}, {"_id": 0})

        if portfolio:
            self.verify_portfolio(portfolio)

            return portfolio

        else:
            empty_portfolio = {
                'id': ID,
                'start_date': int(time.time()),
                'initial_funds': 0,
                'current_value': 0,
                'current_drawdown': 0,
                'trades': [],
                'model_allocations': {  # Equal allocation by default.
                    i.get_name(): (100 / len(self.models)) for i in self.models},
                'risk_per_trade': self.RISK_PER_TRADE,
                'max_correlated_trades': self.MAX_CORRELATED_TRADES,
                'max_accepted_drawdown': self.MAX_ACCEPTED_DRAWDOWN,
                'max_simultaneous_positions': self.MAX_SIMULTANEOUS_POSITIONS,
                'default_stop': self.DEFAULT_STOP}

            self.save_porfolio(empty_portfolio)
            self.logger.debug("Empty portfolio created.")

            return empty_portfolio

    def verify_portfolio(self, portfolio):
        """
        Check stored portfolio data matches actual positions and orders.
        """

        trades = self.db_other['trades'].find({"active": "True"}, {"_id": 0})

        # If trades marked active exist (in DB), check their orders and
        # positions match actual trade state, update portfoilio if disparate.
        if trades:
            for venue in [trade['venue'] for trade in trades]:

                positions = self.exchanges[venue].get_positions()
                orders = self.exchanges[venue].get_orders()

                # TODO: state checking.

        self.save_porfolio(portfolio)
        self.logger.debug(str(
            "Portfolio", portfolio['ID'], "verification complete."))

        return portfolio

    def save_porfolio(self, portfolio):
        """
        Save portfolio state to DB.
        """

        result = self.db_other['portfolio'].replace_one({"id": ID}, portfolio)

        if result['modifiedCount'] == 1:
            self.logger.debug("Portfolio update successful.")
        else:
            self.logger.debug("Portfolio update unsuccessful.")

    def within_risk_limits(self, signal):
        """
        Return true if current holdings are within permissible risk limits.
        """

        for trade in self.pf['trades']['exposure']:
            pass

    def correlated(self, instrument):
        """
        Return true if active trades are correlated to the given instrument.
        """
        pass
