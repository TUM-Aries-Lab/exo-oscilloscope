"""Custom data classes for my module."""

from dataclasses import dataclass


@dataclass
class Vector3:
    """Represent a 3D vector.

    :param x: X component.
    :param y: Y component.
    :param z: Z component.
    """

    x: float
    y: float
    z: float

    def to_tuple(self) -> tuple[float, float, float]:
        """Return the vector as a (x, y, z) tuple.

        :return: Tuple of floats representing the vector.
        """
        return self.x, self.y, self.z


@dataclass
class Quaternion:
    """Represent a quaternion orientation.

    Stored in (x, y, z, w) convention.

    :param x: Quaternion x component.
    :param y: Quaternion y component.
    :param z: Quaternion z component.
    :param w: Quaternion w component.
    """

    x: float
    y: float
    z: float
    w: float

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Return the quaternion as a tuple.

        :return: (x, y, z, w)
        """
        return self.x, self.y, self.z, self.w


@dataclass
class IMUData:
    """Represent a single IMU measurement including accel, gyro, mag, and quaternion.

    :param accel: Accelerometer measurement vector in m/s².
    :param gyro: Gyroscope measurement vector in deg/s.
    :param mag: Magnetometer measurement vector in µT.
    :param quat: Quaternion.
    """

    accel: Vector3
    gyro: Vector3
    mag: Vector3
    quat: Quaternion
    timestamp: float
