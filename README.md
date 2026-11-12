# 🤖 Private Daily GitHub Streak Bot (`daily-streak-tracker`)

This private repository automatically maintains your daily GitHub contribution streak without manual intervention using **Python** (`auto_streak.py`).

## ⚡ How It Works Without Your Intervention (Dual Mode)

1. **Cloud Mode (GitHub Actions — Works even when your laptop is OFF!):**
   * `.github/workflows/daily_streak.yml` runs `python auto_streak.py` automatically every day at **10:00 AM IST (04:30 UTC)**.
   * It makes **1 to 3 commits** per day (randomized so your contribution graph has natural light-green and dark-green shades).
2. **Local PC Mode (Windows Task Scheduler):**
   * Also registered in Windows Task Scheduler (`GitHubDailyStreakBot`) to run automatically when your PC is on.

---

## ⚠️ Crucial One-Time GitHub Profile Setting (For Private Repos!)

Because this repository is **Private**, GitHub hides private commits on your public profile graph unless you turn on this checkbox once:

1. Go to your profile: **https://github.com/Jayasri7-ux**
2. Above your contribution calendar (top-right of the green squares box), click **`Contribution settings`** $\rightarrow$ check **`Private contributions`**.
3. Now every private commit from this bot shows up as green squares on your public profile while keeping the repository invisible to visitors!
