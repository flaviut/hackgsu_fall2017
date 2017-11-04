package com.flaviutamas.dataprocessor;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;

import com.idevicesinc.sweetblue.BleDevice;
import com.idevicesinc.sweetblue.BleDeviceState;
import com.idevicesinc.sweetblue.BleManager;
import com.idevicesinc.sweetblue.BleManagerConfig;
import com.idevicesinc.sweetblue.utils.BluetoothEnabler;

import java.util.Arrays;
import java.util.UUID;


public class MainActivity extends AppCompatActivity {
    private BleManager bleManager;
    private int pot = 0, x = 0, y = 0, z = 0;

    private final UUID DOOR_SERVICE = UUID.fromString("9c856326-4517-407e-a661-faba175acdfe");
    private final UUID POT_CHAR = UUID.fromString("6f9af486-ee00-43ac-8df6-897e05af1aa6");
    private final UUID ACCL_X_CHAR = UUID.fromString("7c38e88a-2724-4aae-96eb-78857589fa3c");
    private final UUID ACCL_Y_CHAR = UUID.fromString("301d6851-ce6d-4fca-9a43-ffe6535b2715");
    private final UUID ACCL_Z_CHAR = UUID.fromString("fe1088ce-68ca-4a4d-ae91-797d046db6e7");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent myIntent = new Intent(this, DeviceScanActivity.class);
        startActivity(myIntent);
/*
        // A ScanFilter decides whether a BleDevice instance will be created from a
        // BLE advertisement and passed to the DiscoveryListener implementation below.
        final BleManagerConfig.ScanFilter scanFilter = new BleManagerConfig.ScanFilter() {
            @Override
            public Please onEvent(ScanEvent e) {
                return Please.acknowledgeIf(e.advertisedServices().contains(DOOR_SERVICE))
                        .thenStopScan();
            }
        };
        final BleManager.DiscoveryListener discoveryListener = new BleManager.DiscoveryListener() {
            @Override
            public void onEvent(DiscoveryEvent event) {
                if (event.was(LifeCycle.DISCOVERED)) {
                    event.device().connect(new BleDevice.StateListener() {
                        @Override
                        public void onEvent(StateEvent event) {
                            Log.d("TEST", "onEvent: " + event.toString());
                            if (event.didEnter(BleDeviceState.CONNECTED)) {
                                Log.i("SweetBlueExample", event.device().getName_debug() + " just initialized!");

                                BleDevice bleDevice = event.device();
                                bleDevice.enableNotify(
                                        Arrays.asList(POT_CHAR, ACCL_X_CHAR, ACCL_Y_CHAR, ACCL_Z_CHAR),
                                        new BleDevice.ReadWriteListener() {
                                            @Override
                                            public void onEvent(ReadWriteEvent e) {
                                                if (e.type() == Type.NOTIFICATION) {
                                                    UUID charUuid = e.charUuid();
                                                    if (charUuid.equals(POT_CHAR)) {
                                                        onChange(e.data_int(false), x, y, z);
                                                    } else if (charUuid.equals(ACCL_X_CHAR)) {
                                                        onChange(pot, e.data_int(false), y, z);
                                                    } else if (charUuid.equals(ACCL_Y_CHAR)) {
                                                        onChange(pot, x, e.data_int(false), z);
                                                    } else if (charUuid.equals(ACCL_Z_CHAR)) {
                                                        onChange(pot, x, y, e.data_int(false));
                                                    }
                                                }
                                            }
                                        });
                            }
                        }
                    });
                }
            }
        };

        BluetoothEnabler.start(this, new BluetoothEnabler.DefaultBluetoothEnablerFilter() {
            @Override
            public Please onEvent(BluetoothEnablerEvent e) {
                if (e.isDone()) {
                    bleManager = e.bleManager();
                    e.bleManager().startScan(scanFilter, discoveryListener);
                }

                return super.onEvent(e);
            }
        });*/
    }

    private void onChange(int newPot, int newX, int newY, int newZ) {
        pot = newPot;
        x = newX;
        y = newY;
        z = newZ;

        TextView currentData = findViewById(R.id.currentData);
        currentData.setText(
                String.format("Potentiometer Value: %d\nAccelerometer values: %d, %d, %d",
                        pot / 1024, x / Short.MAX_VALUE, y / Short.MAX_VALUE, z / Short.MAX_VALUE));
    }
}
