from services import compute_common_availability


def test_three_members_overlap():
    slots = [
        [("16:00", "18:00")],
        [("17:00", "19:00")],
        [("16:30", "18:30")],
    ]
    result = compute_common_availability(slots, min_minutes=30)
    assert result == [("17:00", "18:00")]


def test_touching_intervals_have_no_positive_overlap():
    slots = [[("10:00", "11:00"), ("11:00", "12:00")]]
    result = compute_common_availability(slots, min_minutes=30)
    assert result == []


def test_minimum_duration_filter():
    slots = [
        [("17:00", "17:30")],
        [("17:00", "17:30")],
        [("17:00", "17:30")],
    ]
    result = compute_common_availability(slots, min_minutes=45)
    assert result == []
