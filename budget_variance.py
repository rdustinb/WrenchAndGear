"""
  The purpose of this script is to graphically demonstrate the variability
  of a budget over the course of several months and years to help determine
  the best budgetary values to work off of.

  All numbers can be varied.

  The period should be at least 7 years to show proper full period variance for
  a budget, though in all reality it is much longer (7 * 4 = 28 years) which
  would properly account for leap year variances as well as weekly variance.

  Concepts to consider:
   * Most bills occur monthly, where months are not a standard unit of time.

   * People are often paid biweekly, which is not consistemtly multicative into
  a month.

   * Budgetary items often do not have a set amount, such as groceries or certain
  utilities.

  This script should graph a standard checking accounts balance over the course
  of a long time period, accounting for variance of budget items and harmonic
  stackup of utility debits to income credits.
"""

###############################################################################
"""
  Fixed Amount Debits
    These debits have the same amount every time the bill is received.
"""
def fixed_amount_fixed_period(value, period, offset):
  int_current = offset
  while True:
    if(int_current == (period - 1)):
      int_current = 0
      yield value
    else:
      int_current += 1
      yield 0

import calendar
def fixed_amount_monthly(value, day_of_month, year_offset, month_offset, day_offset):
  int_current_day = day_offset
  int_current_month = month_offset
  int_current_year = year_offset
  while True:
    if(int_current_day == day_of_month):
      # End of the month payment
      yield value
    else:
      yield 0
    # Increment the current date for keeping track of a payment
    if(int_current_day == calendar.monthrange(int_current_year, int_current_month)[1]):
      int_current_day = 1
      if(int_current_month == 12):
        int_current_month = 1
      else:
        int_current_month += 1
      int_current_year += 1
    else:
      int_current_day += 1

###############################################################################
"""
  Variable Amount Debits
    These debits do not have the same amount every time the bill is received.
"""
###############################################################################
"""
  Fixed Amount Credits
    These credits have the same amount every time they are received.
"""
###############################################################################
"""
  Fixed Amount Credits
    These credits do not have the same amount every time they are received.
"""
