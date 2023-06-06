Pin Layouts
-----------

Many scale manufacturers use proprietary pin layouts on serial connectors. This document contains pin layouts for many series of scales by manufacturer. When a pin layout is proprietary, you can either use the manufacturer's cables or make a custom adapter to communicate with the scale. Series marked with a * are compatible with a simple USB-to-Serial adapter without needing manufacturer cables or custom adapters.

=====

Mettler Toledo
--------------

**PG-S**\*

| Pin on Interface | Pin on Scale | Function  |
|------------------|--------------|-----------|
| 2                | 2            | RxD       |
| 3                | 3            | TxD       |
| 4                | 4            | DTR       |
| 5                | 5            | SGND      |
| 6                | 6            | DSR       |
|                  | 7            | Loop to 8 |
|                  | 8            | Loop to 7 |

**Excellence**

| Pin on Interface | Pin on Scale | Function  |
|------------------|--------------|-----------|
| 2                | 2            | RxD       |
| 3                | 3            | TxD       |
| 5                | 5            | SGND      |
| 7                | 8            | CTS       |
| 8                | 7            | RTS       |
|                  | 4            | Loop to 6 |
|                  | 6            | Loop to 4 |

=====

Sartorius
---------

=====

\* Compatible with a simple USB-to-Serial adapter