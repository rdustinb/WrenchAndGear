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
