EESchema Schematic File Version 4
LIBS:control_led-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Transistor_BJT:PN2222A Q1
U 1 1 5BFEECEF
P 3850 2900
F 0 "Q1" H 4041 2854 50  0000 L CNN
F 1 "PN2222A" H 4041 2945 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline_Wide" H 4050 2825 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/PN/PN2222A.pdf" H 3850 2900 50  0001 L CNN
	1    3850 2900
	-1   0    0    1   
$EndComp
$Comp
L Device:R R2
U 1 1 5BFEEDED
P 4400 2900
F 0 "R2" V 4193 2900 50  0000 C CNN
F 1 "R" V 4284 2900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4330 2900 50  0001 C CNN
F 3 "~" H 4400 2900 50  0001 C CNN
	1    4400 2900
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5BFEEE50
P 3750 3450
F 0 "R1" H 3820 3496 50  0000 L CNN
F 1 "R" H 3820 3405 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3680 3450 50  0001 C CNN
F 3 "~" H 3750 3450 50  0001 C CNN
	1    3750 3450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J4
U 1 1 5BFEF05E
P 5400 2900
F 0 "J4" H 5427 2926 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5427 2835 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x02_P1.00mm_Vertical" H 5400 2900 50  0001 C CNN
F 3 "~" H 5400 2900 50  0001 C CNN
	1    5400 2900
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J1
U 1 1 5BFEF0F7
P 2600 2400
F 0 "J1" H 2650 2400 50  0000 C CNN
F 1 "Conn_01x01_Female" H 3050 2300 50  0000 C CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 2600 2400 50  0001 C CNN
F 3 "~" H 2600 2400 50  0001 C CNN
	1    2600 2400
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x01_Female J2
U 1 1 5BFEF168
P 3750 4000
F 0 "J2" V 3597 4048 50  0000 L CNN
F 1 "Conn_01x01_Female" V 3688 4048 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 3750 4000 50  0001 C CNN
F 3 "~" H 3750 4000 50  0001 C CNN
	1    3750 4000
	0    1    1    0   
$EndComp
Wire Wire Line
	3750 3600 3750 3800
Wire Wire Line
	4050 2900 4150 2900
Wire Wire Line
	4550 2900 4700 2900
Wire Wire Line
	3750 3100 3750 3300
$Comp
L Transistor_BJT:2N3904 Q2
U 1 1 5C745034
P 3850 2100
F 0 "Q2" H 4041 2054 50  0000 L CNN
F 1 "2N3904" H 4041 2145 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline_Wide" H 4050 2025 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 3850 2100 50  0001 L CNN
	1    3850 2100
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5C74511A
P 4300 2050
F 0 "R4" V 4093 2050 50  0000 C CNN
F 1 "R" V 4184 2050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4230 2050 50  0001 C CNN
F 3 "~" H 4300 2050 50  0001 C CNN
	1    4300 2050
	0    1    1    0   
$EndComp
$Comp
L Device:R R7
U 1 1 5C7451A1
P 4700 2050
F 0 "R7" V 4493 2050 50  0000 C CNN
F 1 "R" V 4584 2050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 2050 50  0001 C CNN
F 3 "~" H 4700 2050 50  0001 C CNN
	1    4700 2050
	0    1    1    0   
$EndComp
$Comp
L Device:R R11
U 1 1 5C74521A
P 5100 2050
F 0 "R11" V 4893 2050 50  0000 C CNN
F 1 "R" V 4984 2050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 2050 50  0001 C CNN
F 3 "~" H 5100 2050 50  0001 C CNN
	1    5100 2050
	0    1    1    0   
$EndComp
$Comp
L Device:R R9
U 1 1 5C74527B
P 4850 2900
F 0 "R9" V 4643 2900 50  0000 C CNN
F 1 "R" V 4734 2900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4780 2900 50  0001 C CNN
F 3 "~" H 4850 2900 50  0001 C CNN
	1    4850 2900
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x01_Female J9
U 1 1 5C745A93
P 5550 2050
F 0 "J9" H 5577 2076 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5577 1985 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 5550 2050 50  0001 C CNN
F 3 "~" H 5550 2050 50  0001 C CNN
	1    5550 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 2100 4100 2100
Wire Wire Line
	4450 2050 4550 2050
Wire Wire Line
	4850 2050 4950 2050
Wire Wire Line
	5250 2050 5350 2050
Wire Wire Line
	5000 2900 5200 2900
$Comp
L Device:R R3
U 1 1 5C7460C9
P 3750 1600
F 0 "R3" H 3820 1646 50  0000 L CNN
F 1 "R" H 3820 1555 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3680 1600 50  0001 C CNN
F 3 "~" H 3750 1600 50  0001 C CNN
	1    3750 1600
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J7
U 1 1 5C746159
P 3750 1150
F 0 "J7" V 3597 1198 50  0000 L CNN
F 1 "Conn_01x01_Female" V 3688 1198 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 3750 1150 50  0001 C CNN
F 3 "~" H 3750 1150 50  0001 C CNN
	1    3750 1150
	0    1    -1   0   
$EndComp
$Comp
L Device:R R6
U 1 1 5C746274
P 4400 3150
F 0 "R6" V 4193 3150 50  0000 C CNN
F 1 "R" V 4284 3150 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4330 3150 50  0001 C CNN
F 3 "~" H 4400 3150 50  0001 C CNN
	1    4400 3150
	0    1    1    0   
$EndComp
$Comp
L Device:R R10
U 1 1 5C7462AA
P 4850 3150
F 0 "R10" V 4643 3150 50  0000 C CNN
F 1 "R" V 4734 3150 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4780 3150 50  0001 C CNN
F 3 "~" H 4850 3150 50  0001 C CNN
	1    4850 3150
	0    1    1    0   
$EndComp
$Comp
L Device:R R5
U 1 1 5C7462EC
P 4300 2200
F 0 "R5" V 4093 2200 50  0000 C CNN
F 1 "R" V 4184 2200 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4230 2200 50  0001 C CNN
F 3 "~" H 4300 2200 50  0001 C CNN
	1    4300 2200
	0    1    1    0   
$EndComp
$Comp
L Device:R R8
U 1 1 5C746326
P 4700 2200
F 0 "R8" V 4493 2200 50  0000 C CNN
F 1 "R" V 4584 2200 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 2200 50  0001 C CNN
F 3 "~" H 4700 2200 50  0001 C CNN
	1    4700 2200
	0    1    1    0   
$EndComp
$Comp
L Device:R R12
U 1 1 5C74635E
P 5100 2200
F 0 "R12" V 4893 2200 50  0000 C CNN
F 1 "R" V 4984 2200 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5030 2200 50  0001 C CNN
F 3 "~" H 5100 2200 50  0001 C CNN
	1    5100 2200
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x01_Female J10
U 1 1 5C746398
P 5550 2200
F 0 "J10" H 5577 2226 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5577 2135 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 5550 2200 50  0001 C CNN
F 3 "~" H 5550 2200 50  0001 C CNN
	1    5550 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 2050 4100 2100
Wire Wire Line
	4100 2200 4150 2200
Wire Wire Line
	4100 2050 4150 2050
Wire Wire Line
	4450 2200 4550 2200
Wire Wire Line
	4850 2200 4950 2200
Wire Wire Line
	4150 2900 4150 3150
Wire Wire Line
	4150 3150 4250 3150
Connection ~ 4150 2900
Wire Wire Line
	4150 2900 4250 2900
Wire Wire Line
	4550 3150 4700 3150
$Comp
L Connector:Conn_01x01_Female J8
U 1 1 5C746C8E
P 5400 3150
F 0 "J8" H 5427 3176 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5427 3085 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 5400 3150 50  0001 C CNN
F 3 "~" H 5400 3150 50  0001 C CNN
	1    5400 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 3150 5200 3150
Connection ~ 4100 2100
Wire Wire Line
	4100 2100 4100 2200
Wire Wire Line
	3750 1750 3750 1900
Wire Wire Line
	3750 1350 3750 1450
Wire Wire Line
	5250 2200 5350 2200
$Comp
L Connector:Conn_01x01_Female J5
U 1 1 5C74A5CB
P 2600 2700
F 0 "J5" H 2600 2800 50  0000 L CNN
F 1 "Conn_01x01_Female" H 2700 2800 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 2600 2700 50  0001 C CNN
F 3 "~" H 2600 2700 50  0001 C CNN
	1    2600 2700
	-1   0    0    1   
$EndComp
Wire Wire Line
	2800 2700 2800 2600
Connection ~ 3750 2500
Wire Wire Line
	3750 2500 3750 2700
Wire Wire Line
	3750 2300 3750 2500
Wire Wire Line
	2800 2500 3750 2500
Wire Wire Line
	2800 2400 2800 2500
Connection ~ 2800 2500
$Comp
L Connector:Conn_01x01_Female J3
U 1 1 5C74C07E
P 2600 2500
F 0 "J3" H 2600 2500 50  0000 L CNN
F 1 "Conn_01x01_Female" H 2700 2500 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 2600 2500 50  0001 C CNN
F 3 "~" H 2600 2500 50  0001 C CNN
	1    2600 2500
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x01_Female J6
U 1 1 5C74C0C0
P 2600 2600
F 0 "J6" H 2600 2600 50  0000 L CNN
F 1 "Conn_01x01_Female" H 2700 2600 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Horizontal" H 2600 2600 50  0001 C CNN
F 3 "~" H 2600 2600 50  0001 C CNN
	1    2600 2600
	-1   0    0    1   
$EndComp
$EndSCHEMATC
