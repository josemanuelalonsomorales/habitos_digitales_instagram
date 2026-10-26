import pandas as pd
import numpy as np


def calculate_time_metrics(df_posts, df_comments):
    day_map = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
        "Lunes": "Lunes",
        "Martes": "Martes",
        "Miércoles": "Miércoles",
        "Jueves": "Jueves",
        "Viernes": "Viernes",
        "Sábado": "Sábado",
        "Domingo": "Domingo"
    }

    frames = []

    if not df_posts.empty and "timestamp" in df_posts.columns:
        temp_posts = df_posts[["timestamp", "hour", "day_name", "is_weekend"]].copy()
        temp_posts["type"] = "Post Like"
        frames.append(temp_posts)

    if not df_comments.empty and "timestamp" in df_comments.columns:
        temp_comments = df_comments[["timestamp", "hour", "day_name"]].copy()
        temp_comments["is_weekend"] = temp_comments["timestamp"].dt.dayofweek >= 5
        temp_comments["type"] = "Comment Like"
        frames.append(temp_comments)

    if not frames:
        return {}

    df_all = pd.concat(frames, ignore_index=True)
    df_all["day_name"] = df_all["day_name"].map(
        lambda day: day_map.get(day, day)
    )

    total_interactions = len(df_all)
    night_mask = (df_all["hour"] >= 0) & (df_all["hour"] <= 6)
    work_mask = (
        (df_all["hour"] >= 9)
        & (df_all["hour"] <= 18)
        & (~df_all["is_weekend"])
    )
    weekend_mask = df_all["is_weekend"]

    mode_hour = df_all["hour"].mode()
    peak_hour = int(mode_hour.iloc[0]) if not mode_hour.empty else 0

    mode_day = df_all["day_name"].mode()
    peak_day = str(mode_day.iloc[0]) if not mode_day.empty else ""

    hourly_dist = (
        df_all.groupby(["hour", "type"])
        .size()
        .unstack(fill_value=0)
        .to_dict(orient="index")
    )

    daily_dist = df_all.groupby("day_name").size().to_dict()

    return {
        "total_interactions": total_interactions,
        "night_interactions_count": int(night_mask.sum()),
        "night_interactions_pct": round(
            night_mask.sum() / total_interactions * 100, 2
        ) if total_interactions > 0 else 0,
        "work_hours_interactions_count": int(work_mask.sum()),
        "work_hours_interactions_pct": round(
            work_mask.sum() / total_interactions * 100, 2
        ) if total_interactions > 0 else 0,
        "weekend_interactions_pct": round(
            weekend_mask.sum() / total_interactions * 100, 2
        ) if total_interactions > 0 else 0,
        "weekday_interactions_pct": round(
            (total_interactions - weekend_mask.sum()) / total_interactions * 100, 2
        ) if total_interactions > 0 else 0,
        "peak_hour": peak_hour,
        "peak_day": peak_day,
        "hourly_distribution": hourly_dist,
        "daily_distribution": daily_dist
    }

def calculate_density_metrics(df_posts, df_comments, top_n=10):
    top_post_owners = {}
    top_comment_authors = {}
    
    if not df_posts.empty and "owner" in df_posts.columns:
        valid_owners = df_posts["owner"].dropna()
        valid_owners = valid_owners[valid_owners != ""]
        top_post_owners = valid_owners.value_counts().head(top_n).to_dict()
        
    if not df_comments.empty and "comment_author" in df_comments.columns:
        valid_authors = df_comments["comment_author"].dropna()
        valid_authors = valid_authors[valid_authors != ""]
        top_comment_authors = valid_authors.value_counts().head(top_n).to_dict()
        
    total_unique_post_accounts = df_posts["owner"].nunique() if not df_posts.empty and "owner" in df_posts.columns else 0
    total_unique_comment_authors = df_comments["comment_author"].nunique() if not df_comments.empty and "comment_author" in df_comments.columns else 0
    
    post_concentration = 0
    if not df_posts.empty and len(top_post_owners) > 0:
        top_sum = sum(top_post_owners.values())
        post_concentration = round((top_sum / len(df_posts)) * 100, 2)
        
    comment_concentration = 0
    if not df_comments.empty and len(top_comment_authors) > 0:
        top_sum = sum(top_comment_authors.values())
        comment_concentration = round((top_sum / len(df_comments)) * 100, 2)
        
    return {
        "top_post_accounts": top_post_owners,
        "top_comment_authors": top_comment_authors,
        "unique_post_accounts_count": total_unique_post_accounts,
        "unique_comment_authors_count": total_unique_comment_authors,
        "top10_posts_concentration_pct": post_concentration,
        "top10_comments_concentration_pct": comment_concentration
    }

def calculate_network_advanced_metrics(followers, following, close_friends):
    set_followers = set(followers)
    set_following = set(following)
    set_close = set(close_friends)
    
    len_followers = len(set_followers)
    len_following = len(set_following)
    len_close = len(set_close)
    
    mutual = set_followers.intersection(set_following)
    unfollowed_by_them = set_following - set_followers
    not_following_back_them = set_followers - set_following
    
    close_in_following = set_close.intersection(set_following)
    close_in_followers = set_close.intersection(set_followers)
    close_mutual = set_close.intersection(mutual)
    
    reciprocity_rate = (len(mutual) / len_following * 100) if len_following > 0 else 0
    follow_ratio = (len_followers / len_following) if len_following > 0 else 0
    close_friends_coverage = (len(close_in_following) / len_following * 100) if len_following > 0 else 0
    close_friends_purity = (len(close_mutual) / len_close * 100) if len_close > 0 else 0
    
    return {
        "followers_count": len_followers,
        "following_count": len_following,
        "close_friends_count": len_close,
        "mutual_count": len(mutual),
        "unilateral_following_count": len(unfollowed_by_them),
        "unilateral_followers_count": len(not_following_back_them),
        "reciprocity_rate_pct": round(reciprocity_rate, 2),
        "follower_to_following_ratio": round(follow_ratio, 2),
        "close_friends_coverage_in_following_pct": round(close_friends_coverage, 2),
        "close_friends_purity_pct": round(close_friends_purity, 2),
        "close_friends_not_following_count": len(set_close - set_following)
    }

def calculate_security_metrics(df_logins):
    if df_logins.empty:
        return {}
        
    total_logins = len(df_logins)
    device_counts = df_logins["device"].value_counts().to_dict()
    ip_counts = df_logins["ip"].value_counts().to_dict()
    
    unique_devices = df_logins["device"].nunique()
    unique_ips = df_logins["ip"].nunique()
    
    df_logins_sorted = df_logins.sort_values("timestamp")
    df_logins_sorted["time_diff_hours"] = df_logins_sorted["timestamp"].diff().dt.total_seconds() / 3600
    avg_login_frequency_hours = df_logins_sorted["time_diff_hours"].mean()
    
    night_logins = df_logins[(df_logins["hour"] >= 0) & (df_logins["hour"] <= 6)]
    
    return {
        "total_logins": total_logins,
        "unique_devices_count": unique_devices,
        "unique_ips_count": unique_ips,
        "device_breakdown": device_counts,
        "top_ips": dict(list(ip_counts.items())[:5]),
        "avg_hours_between_logins": round(avg_login_frequency_hours, 2) if not np.isnan(avg_login_frequency_hours) else 0,
        "night_logins_count": len(night_logins),
        "night_logins_pct": round((len(night_logins) / total_logins) * 100, 2) if total_logins > 0 else 0
    }