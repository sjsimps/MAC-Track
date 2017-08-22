
# MAC Tracker

This tool may be used to track and visualize when various devices access your network.

### Visualization

The visualization tool will output a device network access timeline.
The timeline displays each device's MAC address on the vertical axis,
and the time from the beginning of the day til the end of the day on the horizontal axis.
Additionally, the visualizer downloads the most recent IEEE MAC OUI database,
and identifies the manufacturer of each device which has accessed the network.

How to run the visualizer:
```
python mac_timeline.py [your Devices file]
```

### Output:

The below image shows sample device usage on the connected network for a whole day:
![alt_tag](https://github.com/sjsimps/MAC-Track/blob/master/sample_output.png)

The below table corresponds to the above image output, and displays the manufacturer
of each device attached on the network using the most recent IEEE OUI Database:
```
MAC ADDRESS       | MANUFACTURER
------------------|------------------------------------------------
C8:69:CD:A9:37:D2 | Apple, Inc.
C0:EE:FB:25:8C:A5 | OnePlus Tech (Shenzhen) Ltd
C0:BD:D1:35:50:3E | SAMSUNG ELECTRO-MECHANICS(THAILAND)
B0:34:95:E1:3D:5C | Apple, Inc.
A4:5E:60:C6:74:5D | Apple, Inc.
94:EB:CD:49:1F:7B | BlackBerry RTS
90:FD:61:D0:E6:B5 | Apple, Inc.
7C:1E:52:4D:4C:D7 | Microsoft
78:FD:94:CF:B6:44 | Apple, Inc.
60:6C:66:58:36:21 | Intel Corporate
60:2A:D0:73:83:F1 | Cisco SPVTG
34:23:BA:6A:48:91 | SAMSUNG ELECTRO-MECHANICS(THAILAND)
2C:F0:A2:61:A9:2C | Apple, Inc.
```

### Tracking

The tracker must be left running on a device that is actively connected to the network.
This will populate 'Devices' file with timing and access information,
which can be parsed and analyzed using the visualizer.

To run the tracker, use the following command:
```
python mac_tracker.py [i=interface p=poll_rate]
```
Where the interface option may be used to switch the network interface used,
and poll rate determines how frequently the tracker polls the network.

