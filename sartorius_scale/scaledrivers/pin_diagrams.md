Pin Layouts
-----------

Many scale manufacturers use proprietary pin layouts on serial connectors. This document contains pin layouts for many series of scales by manufacturer. When a pin layout is proprietary, you can either use the manufacturer's cables or make a custom adapter to communicate with the scale. Series marked with a * are compatible with a simple USB-to-Serial adapter without needing manufacturer cables or custom adapters.

=====

Mettler Toledo
--------------

**PG-S**\*
9-Pin Serial, Female

| Interface | Flow | Scale | Function |
|-----------|------|-------|----------|
|         2 |  ->  | 2     | TxD      |
|         3 |  <-  | 3     | RxD      |
|         4 |  ->  | 4     | DTR      |
|         5 |  --  | 5     | SGND     |
|         6 |  <-  | 6     | DSR      |
|           |      | 7, 8  | Loop     |

No negative side effects have been noticed from making the 7--8 loop on the scale a straight through.  Switching the pins on 7 and 8 when going from interface to scale makes an adapter that is compatible with this scale and other Mettler Toledo scales, although a special adapter for this scale is not necessary.
To allow communication with this scale from a computer, go to the menu and find the option that says "printer".  Change the option to say "host", and it should be configured correctly from there.

**Excellence**
9-Pin Serial, Female

| Interface | Flow | Scale | Function |
|----------:|:----:|-------|----------|
|         2 |  <-  | 2     | RxD      |
|         3 |  ->  | 3     | TxD      |
|         5 |  --  | 5     | SGND     |
|         7 |  <-  | 8     | CTS      |
|         8 |  ->  | 7     | RTS      |
|           |      | 4, 6  | Loop     |

No negative side effects have been noticed from making the 4--6 loop on the scale a straight through.

=====

Sartorius
---------

**Entris**
25-Pin Serial, Female

DB-9
| Interface | Flow | Scale    | Function |
|----------:|:----:|----------|----------|
|         2 |  <-  | 2        | RxD      |
|         3 |  ->  | 3        | TxD      |
|         4 |  ->  | 5        | CTS      |
|         5 |  --  | 4, 7, 14 | GND      |
|      6, 8 |  <-  | 20       | DTR      |

DB-25
| Interface | Flow | Scale    | Function |
|----------:|:----:|----------|----------|
|         2 |  ->  | 3        | TxD      |
|         3 |  <-  | 2        | RxD      |
|      5, 6 |  <-  | 20       | DTR      |
|         7 |  --  | 4, 7, 14 | GND      |
|        20 |  ->  | 5        | CTS      |

=====

\* Compatible with a simple USB-to-Serial adapter

[Markdown Table Generator](https://www.tablesgenerator.com/markdown_tables)