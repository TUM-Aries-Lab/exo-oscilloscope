"""Custom data classes for my module."""

from dataclasses import dataclass


@dataclass
class Vector3:
    """Represent a 3D vector."""

    x: float
    y: float
    z: float

    def to_tuple(self) -> tuple[float, float, float]:
        """Return the vector as a (x, y, z) tuple."""
        return self.x, self.y, self.z

    def __mul__(self, other: float | int) -> "Vector3":
        """Scalar multiplication: v * scalar.

        :param other: Scalar multiplication.
        :return: Vector3.
        """
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float | int) -> "Vector3":
        """Scalar multiplication: scalar * v.

        :param other: Scalar multiplication.
        :return: Vector3.
        """
        return self.__mul__(other)


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

    def to_tuple(self, scalar_first: bool = False) -> tuple[float, float, float, float]:
        """Return the quaternion as a tuple.

        :param scalar_first: If True, the first component of the quaternion is scalar.
        :return: (x, y, z, w)
        """
        if scalar_first:
            return self.w, self.x, self.y, self.z
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


@dataclass
class MotorState:
    """Represent a single motor state.

    :param torque: Torque measurement vector in m/s.
    :param speed: Motor speed measurement vector in m/s.
    :param position: Motor position measurement vector in m/s.
    :param timestamp: Motor timestamp measurement vector in ms.
    """

    torque: float
    speed: float
    position: float
    timestamp: float


@dataclass
class PlotConfig:
    """Configuration for a single pyqtgraph plot."""

    title_prefix: str
    y_label: str
    signals: list[str]
    pens: list
    buffer_size: int
