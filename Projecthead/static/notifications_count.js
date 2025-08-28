document.addEventListener("DOMContentLoaded", () => {
    const unreadCount = document.getElementById("unread-count");
    const notificationLink = document.getElementById("open-notifications");

    if (!unreadCount) {
        console.log("No #unread-count element found, likely unauthenticated user.");
        return;
    }

    const fetchUnreadCount = () => {
        fetch("/notifications/get/", {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const count = data.notifications_count || 0;
                unreadCount.style.display = count > 0 ? "inline-block" : "none";
                unreadCount.textContent = count;
                console.log(`Notification count updated: ${count}`);
            })
            .catch(error => {
                console.error("Error fetching notification count:", error.message);
            });
    };

    const markAllAsRead = () => {
        fetch("/notifications/mark_all_read/", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    unreadCount.style.display = "none";
                    unreadCount.textContent = "0";
                    console.log("All notifications marked as read, count set to 0");
                }
            })
            .catch(error => {
                console.error("Error marking notifications as read:", error.message);
            });
    };

    // Initial fetch
    fetchUnreadCount();
    // Refresh every 1 minute
    setInterval(fetchUnreadCount, 60000);

    // Refresh count on page focus or visibility change
    window.addEventListener("focus", fetchUnreadCount);
    document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible") {
            fetchUnreadCount();
        }
    });

    // Mark all as read when clicking notifications link
    if (notificationLink) {
        notificationLink.addEventListener("click", (e) => {
            // Allow navigation to proceed, mark as read asynchronously
            markAllAsRead();
        });
    }
});