import locale
from datetime import date, datetime, timedelta

from convertdate import islamic

from constants import (
    CURR_ISLAMIC_MONTH,
    CURR_ISLAMIC_YEAR,
    DEFAULT_LEAVE_DAYS,
    NEXT_YEAR,
    TODAY,
)

locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")


def get_ramadan_celebrations() -> list[str]:
    """Get celebration dates of Ramadan."""
    if CURR_ISLAMIC_MONTH < 9:
        ramadan_year = CURR_ISLAMIC_YEAR
    else:
        ramadan_year = CURR_ISLAMIC_YEAR + 1

    ramadan_end = islamic.to_gregorian(ramadan_year, 10, 1)
    ramadan_end_date = date(*ramadan_end) - timedelta(days=1)

    date_range = []
    for i in range(3):
        celeb_date = ramadan_end_date + timedelta(days=i)
        date_range.append(celeb_date.isoformat())

    return date_range


def get_eid_al_adha_celebrations() -> list[str]:
    """Get celebration dates of Eid al-Adha."""
    if (CURR_ISLAMIC_MONTH < 12) or (
        CURR_ISLAMIC_MONTH == 12
        and islamic.to_gregorian(CURR_ISLAMIC_YEAR, 12, 9) > TODAY
    ):
        eid_al_adha_year = CURR_ISLAMIC_YEAR
    else:
        eid_al_adha_year = CURR_ISLAMIC_YEAR + 1

    eid_al_adha_date = islamic.to_gregorian(eid_al_adha_year, 12, 9)

    next_eid_al_adha = date(*eid_al_adha_date)

    date_range = []
    for i in range(4):
        date_eid_al_adha = next_eid_al_adha + timedelta(days=i)
        date_range.append(date_eid_al_adha.isoformat())
    return date_range


holidays = {
    "Yılbaşı": f"{NEXT_YEAR}-01-01",
    "Ramazan Bayramı": get_ramadan_celebrations(),
    "Ulusal Egemenlik ve Çocuk Bayramı": f"{NEXT_YEAR}-04-23",
    "İşçi Bayramı": f"{NEXT_YEAR}-05-01",
    "Gençlik ve Spor Bayramı": f"{NEXT_YEAR}-05-19",
    "Kurban Bayramı": get_eid_al_adha_celebrations(),
    "Demokrasi ve Milli Birlik Günü": f"{NEXT_YEAR}-07-15",
    "Zafer Bayramı": f"{NEXT_YEAR}-08-30",
    "Cumhuriyet Bayramı": [f"{NEXT_YEAR}-10-29"],
}


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d")


def find_efficient_leaves(max_leaves: int = DEFAULT_LEAVE_DAYS) -> list[date]:
    """Find efficient leave days based on holidays and weekends."""
    all_holiday_dates = set()

    # Convert all holidays to datetime objects
    for holiday, dates in holidays.items():
        if isinstance(dates, list):
            for date in dates:
                all_holiday_dates.add(str_to_date(date))
        else:
            all_holiday_dates.add(str_to_date(dates))

    # Generate all possible leave opportunities with scoring
    potential_leaves = []
    sorted_dates = sorted(list(all_holiday_dates))

    # First, identify all holiday clusters (including weekends)
    clusters = []
    current_cluster = set()

    start_date = min(sorted_dates) - timedelta(days=10)
    end_date = max(sorted_dates) + timedelta(days=10)
    current = start_date

    # Build initial clusters including weekends
    while current <= end_date:
        is_off = False
        if current in all_holiday_dates or current.weekday() >= 5:
            is_off = True

        if is_off:
            current_cluster.add(current)
        elif current_cluster:
            clusters.append(current_cluster)
            current_cluster = set()

        current += timedelta(days=1)

    if current_cluster:
        clusters.append(current_cluster)

    # Find gaps between clusters that are worth bridging
    for i in range(len(clusters) - 1):
        cluster1 = max(clusters[i])
        cluster2 = min(clusters[i + 1])
        gap_days = (cluster2 - cluster1).days - 1
        working_days = sum(
            1
            for d in range(1, gap_days + 1)
            if (cluster1 + timedelta(days=d)).weekday() < 5
        )

        # More aggressive bridging - consider gaps up to 7 working days
        if working_days <= 7:
            current = cluster1 + timedelta(days=1)
            while current < cluster2:
                if current.weekday() < 5 and current not in all_holiday_dates:
                    # Score based on potential for long stretches
                    score = 15 - working_days  # Higher score for smaller gaps

                    # Bonus points for creating longer consecutive periods
                    days_before = sum(
                        1 for d in clusters[i] if d >= current - timedelta(days=7)
                    )
                    days_after = sum(
                        1 for d in clusters[i + 1] if d <= current + timedelta(days=7)
                    )

                    if days_before + days_after >= 7:  # If potential for week+ stretch
                        score += 5
                    if days_before + days_after >= 10:  # If potential for 10+ days
                        score += 5

                    potential_leaves.append((current, score))
                current += timedelta(days=1)

    # Sort by score (higher is better) and select best days
    potential_leaves.sort(key=lambda x: (-x[1], x[0]))
    proposed_leaves = []
    leaves_count = 0

    # Take days that create longest stretches first
    for date, _ in potential_leaves:
        if leaves_count >= max_leaves:
            break
        if date not in proposed_leaves:
            proposed_leaves.append(date)
            leaves_count += 1

    return sorted(proposed_leaves)


def calculate_consecutive_days(
    proposed_leaves: list[date],
    all_holidays: list[date],
) -> list[list[date]]:
    """Calculate consecutive days from proposed leaves and all holidays."""
    consecutive_periods = []
    current_period = []

    # Combine all dates including weekends
    all_dates = set()

    # Add all holidays and proposed leaves
    all_dates.update(proposed_leaves)
    all_dates.update(all_holidays)

    # Add all weekends between min and max dates
    if all_dates:
        start_date = min(all_dates) - timedelta(days=7)  # Look back one week
        end_date = max(all_dates) + timedelta(days=7)  # Look ahead one week
        current = start_date

        while current <= end_date:
            if current.weekday() >= 5:  # Saturday or Sunday
                all_dates.add(current)
            current += timedelta(days=1)

    # Sort all dates
    all_dates = sorted(list(all_dates))

    # Find consecutive periods
    for dt in all_dates:
        if not current_period:
            current_period = [dt]
        else:
            prev_date = current_period[-1]
            if (dt - prev_date).days == 1:
                current_period.append(dt)
            else:
                if len(current_period) >= 3:  # Only keep periods of 3+ days
                    consecutive_periods.append(current_period)
                current_period = [dt]

    if current_period and len(current_period) >= 3:
        consecutive_periods.append(current_period)

    return consecutive_periods


def main():
    """Main function to calculate efficient leave days and display statistics."""
    try:
        max_leaves = int(
            input("Maksimum izin günü sayısını girin (varsayılan 14): ").strip() or "14"
        )
    except ValueError:
        print("Geçersiz giriş. Varsayılan değer olan 14 gün kullanılacak.")
        max_leaves = 14

    proposed_leaves = find_efficient_leaves(max_leaves)

    print(
        f"\n{NEXT_YEAR} için Önerilen İzin Günleri ({max_leaves} günün {len(proposed_leaves)} günü kullanılıyor):"
    )
    print("\n".join([f"- {dt.strftime('%d %B %Y, %A')}" for dt in proposed_leaves]))

    all_holidays = [
        str_to_date(date)
        for holiday in holidays.values()
        for date in (holiday if isinstance(holiday, list) else [holiday])
    ]

    # Toplam tatil günlerini hesapla
    all_off_days = set()

    # Tüm haftasonlarını ekle
    current = datetime(NEXT_YEAR, 1, 1)
    end = datetime(NEXT_YEAR, 12, 31)
    while current <= end:
        if current.weekday() >= 5:  # Cumartesi veya Pazar
            all_off_days.add(current)
        current += timedelta(days=1)

    # Resmi tatiller ve önerilen izinleri ekle
    all_off_days.update(all_holidays)
    all_off_days.update(proposed_leaves)

    consecutive_periods = calculate_consecutive_days(proposed_leaves, all_holidays)

    print("\nUzun Hafta Sonu/Tatil Dönemleri:")
    total_consecutive_days = 0
    for period in consecutive_periods:
        start = period[0]
        end = period[-1]
        days = (end - start).days + 1
        total_consecutive_days += days
        print(
            f"- {start.strftime('%d %B %Y')} ile {end.strftime('%d %B %Y')} arası: {days} gün",
        )

    print(f"\nToplam ardışık tatil günleri: {total_consecutive_days}")
    print(
        f"{NEXT_YEAR} yılı içerisinde bulunan toplam tatil günleri (tüm haftasonları + resmi tatiller + izinler): {len(all_off_days)}"
    )


if __name__ == "__main__":
    main()
