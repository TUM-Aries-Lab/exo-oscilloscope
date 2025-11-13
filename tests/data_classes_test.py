"""Test the custom data classes."""

from exo_oscilloscope.data_classes import IMUData, Quaternion, Vector3


def test_vector3() -> None:
    """Test Vector3 initialization."""
    # Arrange
    accel = Vector3(0, 0, 0)

    # Act
    accel_tuple = accel.to_tuple()

    # Assert
    assert accel_tuple == (0, 0, 0)


def test_quaternion() -> None:
    """Test Quaternion initialization."""
    # Arrange
    quat = Quaternion(0, 0, 0, 0)

    # Act
    quat_tuple = quat.to_tuple()

    # Assert
    assert quat_tuple == (0, 0, 0, 0)


def test_imu_data() -> None:
    """Test IMU Data initialization."""
    # Arrange
    accel = Vector3(0, 0, 0)
    gyro = Vector3(0, 0, 0)
    mag = Vector3(0, 0, 0)
    quat = Quaternion(0, 0, 0, 0)
    t = 0.0

    # Act
    imu = IMUData(accel=accel, gyro=gyro, mag=mag, quat=quat, timestamp=t)

    # Assert
    assert imu.accel == accel
    assert imu.gyro == gyro
    assert imu.mag == mag
    assert imu.quat == quat
    assert imu.timestamp == t
