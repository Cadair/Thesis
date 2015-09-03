from collections import namedtuple

__all__ = ['sim_params']

PeriodAmp = namedtuple('PeriodAmp', ['period', 'amp', 'fort_amp'])

periods=(30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0, 360.0, 390.0, 420.0, 450.0, 480.0, 510.0, 540.0, 570.0, 600.0)
amps=('A20r2', 'A20', 'A20r2-3', 'A10r2', 'A4r10', 'A20-r3', 'A20r2-7', 'A10', 'A20-3r2', 'A4r5', 'A20r2-11', 'A10r2-3', 'A20r2-13', 'A20-r7', 'A4r10-3', 'A5r2', 'A20r2-17', 'A20-3', 'A20r2-19', 'A2r10')
fortamps=("20.d0 * SQRT(2.d0)", "20.d0", "20.d0 * SQRT(2.d0 / 3.d0)", "10.d0 * SQRT(2.d0)", "4.d0 * SQRT(10.d0)", "20.d0 / SQRT(3.d0)", "20.d0 * SQRT(2.d0 / 7.d0)", "10.d0", "20.d0 / 3.d0 * SQRT(2.d0)", "4.d0 * SQRT(5.d0)", "20.d0 * SQRT(2.d0 /11.d0)", "10.d0 * SQRT(2.d0 / 3.d0)", "20.d0 * SQRT(2.d0 / 13.d0)", "20.d0 / SQRT(7.d0)", "4.d0 * SQRT(10.d0 / 3.d0)", "5.d0 * SQRT(2.d0)", "20.d0 * SQRT(2.d0 / 17.d0)", "20.d0 / 3.d0", "20.d0 * SQRT(2.d0 / 19.d0)", "2.d0 * SQRT(10.d0)")

# These are the same as the parameters in cfg.
sim_params = tuple([PeriodAmp(period=p, amp=a, fort_amp=fa) for p,a,fa in zip(periods, amps, fortamps)])


str_amps = (r"$20\sqrt{2}$", r"$20$", r"$20\sqrt{\frac{2}{3}}$", r"$10\sqrt{2}$", r"$4\sqrt{10}$", r"$\frac{20}{\sqrt{3}}$", r"$20\sqrt{\frac{2}{7}}$", r"$10$", r"$\frac{20}{3}\sqrt{2}$", r"$4\sqrt{5}$", r"$20\sqrt{\frac{2}{11}}$", r"", r"", r"", r"", r"", r"", r"", r"", r"")
