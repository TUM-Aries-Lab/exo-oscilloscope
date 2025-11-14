"""Test the custom data classes."""

import pytest

from exo_oscilloscope.data_classes import IMUData, Quaternion, Vector3


def test_vector3() -> None:
    """Test Vector3 initialization."""
    # Arrange
    accel = Vector3(0, 0, 0)

    # Act
    accel_tuple = accel.to_tuple()

    # Assert
    assert accel_tuple == (0, 0, 0)


def test_vector3_multi() -> None:
    """Test Vector3 multiplication."""
    # Arrange
    accel = Vector3(0, 0, 0)

    # Act
    left = 3 * accel
    right = accel * 3

    # Assert
    assert left == right


@pytest.mark.parametrize("scalar_first", [True, False])
def test_quaternion(scalar_first: bool) -> None:
    """Test Quaternion initialization."""
    # Arrange
    quat = Quaternion(x=0, y=0, z=0, w=1)

    # Act
    quat_tuple = quat.to_tuple(scalar_first=scalar_first)

    # Assert
    assert quat_tuple == (int(scalar_first), 0, 0, int(not scalar_first))


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
