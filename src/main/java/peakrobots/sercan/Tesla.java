package peakrobots.sercan;

import robocode.*;
import robocode.Robot;

import java.awt.*;

import static robocode.util.Utils.normalRelativeAngleDegrees;

public class Tesla extends Robot {
    private int count = 0;
    private double gunTurnDegree;
    private String enemyName;

    public void run() {
        setBodyColor(Color.blue);
        setGunColor(Color.yellow);
        setRadarColor(Color.cyan);
        setScanColor(Color.white);
        setBulletColor(Color.blue);

        enemyName = null;
        setAdjustGunForRobotTurn(true);
        gunTurnDegree = 10;

        while (true) {
            turnGunRight(gunTurnDegree);
            count++;
            scanEnemies();
        }
    }

    private void scanEnemies() {
        if (count > 2) {
            gunTurnDegree = -10;
        }
        if (count > 5) {
            gunTurnDegree = 10;
        }
        if (count > 11) {
            enemyName = null;
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {

        if (enemyName != null && !e.getName().equals(enemyName)) {
            return;
        }

        if (enemyName == null) {
            enemyName = e.getName();
        }
        count = 0;
        if (e.getDistance() > 150) {
            gunTurnDegree = normalRelativeAngleDegrees(e.getBearing() + (getHeading() - getRadarHeading()));

            turnGunRight(gunTurnDegree);
            turnRight(e.getBearing());
            ahead(e.getDistance() - 140);
            return;
        }

        gunTurnDegree = normalRelativeAngleDegrees(e.getBearing() + (getHeading() - getRadarHeading()));
        turnGunRight(gunTurnDegree);
        fire(3);

        if (isTooClose(e)) {
            if (e.getBearing() > -90 && e.getBearing() <= 90) {
                back(40);
            } else {
                ahead(40);
            }
        }
        scan();
    }

    private boolean isTooClose(ScannedRobotEvent e) {
        return e.getDistance() < 100;
    }

    public void onHitRobot(HitRobotEvent e) {
        enemyName = e.getName();
        gunTurnDegree = normalRelativeAngleDegrees(e.getBearing() + (getHeading() - getRadarHeading()));
        turnGunRight(gunTurnDegree);
        fire(3);
        back(50);
    }
}
