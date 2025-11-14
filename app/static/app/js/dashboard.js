// Initialize Lucide Icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Initialize sidebar state
    initSidebar();
    
    // Initialize theme
    initTheme();
    
    // Initialize collapsible menus
    initCollapsibleMenus();
    
    // Initialize user dropdown
    initUserDropdown();
    
    // Initialize notification dropdown
    initNotificationDropdown();
    
    // Initialize charts
    initCharts();
    
    // Initialize mobile sidebar
    initMobileSidebar();
});

// Sidebar functionality
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarTrigger = document.getElementById('sidebarTrigger');
    const logoText = document.getElementById('logoText');
    
    // Load sidebar state from localStorage
    const savedState = localStorage.getItem('sidebarState');
    if (savedState === 'collapsed') {
        sidebar.setAttribute('data-state', 'collapsed');
    }
    
    // Toggle sidebar
    if (sidebarTrigger) {
        sidebarTrigger.addEventListener('click', function() {
            const currentState = sidebar.getAttribute('data-state');
            const newState = currentState === 'expanded' ? 'collapsed' : 'expanded';
            sidebar.setAttribute('data-state', newState);
            localStorage.setItem('sidebarState', newState);
            
            // Update icons after state change
            setTimeout(() => {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 100);
        });
    }
}

// Mobile Sidebar
function initMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarTrigger = document.getElementById('sidebarTrigger');
    const sidebarWrapper = document.getElementById('sidebarWrapper');
    
    // Create overlay if it doesn't exist
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        sidebarWrapper.appendChild(overlay);
    }
    
    function isMobile() {
        return window.innerWidth < 768;
    }
    
    function openMobileSidebar() {
        if (isMobile()) {
            sidebar.classList.add('mobile-open');
            overlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeMobileSidebar() {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
    }
    
    // Toggle mobile sidebar
    if (sidebarTrigger) {
        sidebarTrigger.addEventListener('click', function() {
            if (isMobile()) {
                if (sidebar.classList.contains('mobile-open')) {
                    closeMobileSidebar();
                } else {
                    openMobileSidebar();
                }
            }
        });
    }
    
    // Close on overlay click
    overlay.addEventListener('click', closeMobileSidebar);
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            closeMobileSidebar();
        }
    });
}

// Theme functionality
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        if (themeIcon) {
            themeIcon.setAttribute('data-lucide', 'sun');
        }
    } else {
        document.documentElement.classList.remove('dark');
        if (themeIcon) {
            themeIcon.setAttribute('data-lucide', 'moon');
        }
    }
    
    // Update icon after theme is set
    setTimeout(() => {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }, 100);
    
    // Toggle theme
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isDark = document.documentElement.classList.contains('dark');
            
            if (isDark) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                if (themeIcon) {
                    themeIcon.setAttribute('data-lucide', 'moon');
                }
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                if (themeIcon) {
                    themeIcon.setAttribute('data-lucide', 'sun');
                }
            }
            
            // Update icons
            setTimeout(() => {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 100);
        });
    }
}

// Collapsible menu functionality
function initCollapsibleMenus() {
    const collapsibleTriggers = document.querySelectorAll('.collapsible-trigger');
    
    collapsibleTriggers.forEach(trigger => {
        const menuItem = trigger.closest('.menu-item');
        
        // Set initial state
        menuItem.setAttribute('data-open', 'false');
        
        trigger.addEventListener('click', function() {
            const isOpen = menuItem.getAttribute('data-open') === 'true';
            menuItem.setAttribute('data-open', isOpen ? 'false' : 'true');
            
            // Update icons
            setTimeout(() => {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 100);
        });
    });
}

// User dropdown functionality
function initUserDropdown() {
    const userMenuTrigger = document.getElementById('userMenuTrigger');
    const userDropdown = document.getElementById('userDropdown');
    
    if (userMenuTrigger && userDropdown) {
        userMenuTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            // Close notification dropdown if open
            const notificationDropdown = document.getElementById('notificationDropdown');
            if (notificationDropdown && notificationDropdown.classList.contains('show')) {
                notificationDropdown.classList.remove('show');
            }
            userDropdown.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenuTrigger.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }
}

// Notification dropdown functionality
function initNotificationDropdown() {
    const notificationTrigger = document.getElementById('notificationTrigger');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationBackdrop = document.getElementById('notificationBackdrop');
    const notificationBadge = document.querySelector('.notification-badge');
    const markAllButton = document.querySelector('.notification-mark-all');
    const notificationItems = document.querySelectorAll('.notification-item');
    
    function isMobile() {
        return window.innerWidth < 768;
    }
    
    function openNotification() {
        notificationDropdown.classList.add('show');
        if (isMobile() && notificationBackdrop) {
            notificationBackdrop.classList.add('show');
            document.body.style.overflow = 'hidden';
            // Force reflow to ensure styles are applied
            notificationDropdown.offsetHeight;
        }
        // Update icons after opening
        setTimeout(() => {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }, 50);
    }
    
    function closeNotification() {
        notificationDropdown.classList.remove('show');
        if (notificationBackdrop) {
            notificationBackdrop.classList.remove('show');
        }
        document.body.style.overflow = '';
    }
    
    if (notificationTrigger && notificationDropdown) {
        notificationTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            // Close user dropdown if open
            const userDropdown = document.getElementById('userDropdown');
            if (userDropdown && userDropdown.classList.contains('show')) {
                userDropdown.classList.remove('show');
            }
            
            if (notificationDropdown.classList.contains('show')) {
                closeNotification();
            } else {
                openNotification();
            }
            
            // Update icons after toggle
            setTimeout(() => {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 100);
        });
        
        // Close on backdrop click (mobile)
        if (notificationBackdrop) {
            notificationBackdrop.addEventListener('click', function() {
                closeNotification();
            });
        }
        
        // Close button functionality
        const notificationClose = document.getElementById('notificationClose');
        if (notificationClose) {
            notificationClose.addEventListener('click', function(e) {
                e.stopPropagation();
                closeNotification();
            });
        }
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!notificationTrigger.contains(e.target) && !notificationDropdown.contains(e.target)) {
                closeNotification();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (!isMobile() && notificationBackdrop) {
                notificationBackdrop.classList.remove('show');
            }
        });
        
        // Mark all as read functionality
        if (markAllButton) {
            markAllButton.addEventListener('click', function(e) {
                e.stopPropagation();
                notificationItems.forEach(item => {
                    item.classList.remove('unread');
                });
                
                // Update badge count
                if (notificationBadge) {
                    notificationBadge.textContent = '0';
                    if (notificationBadge.textContent === '0') {
                        notificationBadge.style.display = 'none';
                    }
                }
            });
        }
        
        // Mark individual notification as read
        notificationItems.forEach(item => {
            item.addEventListener('click', function() {
                if (this.classList.contains('unread')) {
                    this.classList.remove('unread');
                    
                    // Update badge count
                    const unreadCount = document.querySelectorAll('.notification-item.unread').length;
                    if (notificationBadge) {
                        if (unreadCount > 0) {
                            notificationBadge.textContent = unreadCount;
                            notificationBadge.style.display = 'flex';
                        } else {
                            notificationBadge.style.display = 'none';
                        }
                    }
                }
            });
        });
    }
}

// Charts initialization
function initCharts() {
    // Wait for React, ReactDOM, and Recharts to be available
    if (typeof React === 'undefined' || typeof ReactDOM === 'undefined' || typeof Recharts === 'undefined') {
        setTimeout(initCharts, 100);
        return;
    }
    
    const { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } = Recharts;
    
    // Sales data
    const salesData = [
        { month: "Jan", value: 200 },
        { month: "Feb", value: 400 },
        { month: "Mar", value: 300 },
        { month: "Apr", value: 450 },
        { month: "May", value: 350 },
        { month: "Jun", value: 380 },
        { month: "Jul", value: 500 },
        { month: "Aug", value: 150 },
        { month: "Sep", value: 320 },
        { month: "Oct", value: 550 },
        { month: "Nov", value: 480 },
        { month: "Dec", value: 280 },
    ];
    
    // Statistics data
    const statisticsData = [
        { month: "Jan", value1: 180, value2: 50 },
        { month: "Feb", value1: 185, value2: 55 },
        { month: "Mar", value1: 175, value2: 60 },
        { month: "Apr", value1: 190, value2: 70 },
        { month: "May", value1: 195, value2: 80 },
        { month: "Jun", value1: 200, value2: 90 },
        { month: "Jul", value1: 220, value2: 100 },
        { month: "Aug", value1: 230, value2: 110 },
        { month: "Sep", value1: 240, value2: 120 },
        { month: "Oct", value1: 250, value2: 130 },
        { month: "Nov", value1: 260, value2: 140 },
        { month: "Dec", value1: 270, value2: 150 },
    ];
    
    // Get current theme colors
    function getThemeColors() {
        const isDark = document.documentElement.classList.contains('dark');
        
        return {
            border: isDark ? 'hsl(217, 33%, 20%)' : 'hsl(220, 13%, 91%)',
            mutedForeground: isDark ? 'hsl(215, 20%, 65%)' : 'hsl(217, 10%, 55%)',
            primary: 'hsl(221, 83%, 53%)',
            card: isDark ? 'hsl(217, 33%, 15%)' : 'hsl(0, 0%, 100%)',
            radius: '0.5rem'
        };
    }
    
    // Initialize Bar Chart
    const barChartContainer = document.getElementById('barChart');
    if (barChartContainer && barChartContainer.children.length === 0) {
        const colors = getThemeColors();
        
        ReactDOM.render(
            React.createElement(ResponsiveContainer, { width: "100%", height: 300 },
                React.createElement(BarChart, { data: salesData },
                    React.createElement(CartesianGrid, { strokeDasharray: "3 3", stroke: colors.border }),
                    React.createElement(XAxis, { dataKey: "month", stroke: colors.mutedForeground }),
                    React.createElement(YAxis, { stroke: colors.mutedForeground }),
                    React.createElement(Tooltip, {
                        contentStyle: {
                            backgroundColor: colors.card,
                            border: `1px solid ${colors.border}`,
                            borderRadius: colors.radius
                        }
                    }),
                    React.createElement(Bar, { 
                        dataKey: "value", 
                        fill: colors.primary, 
                        radius: [8, 8, 0, 0] 
                    })
                )
            ),
            barChartContainer
        );
    }
    
    // Initialize Area Chart
    const areaChartContainer = document.getElementById('areaChart');
    if (areaChartContainer && areaChartContainer.children.length === 0) {
        const colors = getThemeColors();
        
        ReactDOM.render(
            React.createElement(ResponsiveContainer, { width: "100%", height: 300 },
                React.createElement(AreaChart, { data: statisticsData },
                    React.createElement('defs', null,
                        React.createElement('linearGradient', { id: "colorValue1", x1: "0", y1: "0", x2: "0", y2: "1" },
                            React.createElement('stop', { offset: "5%", stopColor: colors.primary, stopOpacity: 0.3 }),
                            React.createElement('stop', { offset: "95%", stopColor: colors.primary, stopOpacity: 0 })
                        ),
                        React.createElement('linearGradient', { id: "colorValue2", x1: "0", y1: "0", x2: "0", y2: "1" },
                            React.createElement('stop', { offset: "5%", stopColor: colors.primary, stopOpacity: 0.15 }),
                            React.createElement('stop', { offset: "95%", stopColor: colors.primary, stopOpacity: 0 })
                        )
                    ),
                    React.createElement(CartesianGrid, { strokeDasharray: "3 3", stroke: colors.border }),
                    React.createElement(XAxis, { dataKey: "month", stroke: colors.mutedForeground }),
                    React.createElement(YAxis, { stroke: colors.mutedForeground }),
                    React.createElement(Tooltip, {
                        contentStyle: {
                            backgroundColor: colors.card,
                            border: `1px solid ${colors.border}`,
                            borderRadius: colors.radius
                        }
                    }),
                    React.createElement(Area, {
                        type: "monotone",
                        dataKey: "value1",
                        stroke: colors.primary,
                        fillOpacity: 1,
                        fill: "url(#colorValue1)"
                    }),
                    React.createElement(Area, {
                        type: "monotone",
                        dataKey: "value2",
                        stroke: colors.primary,
                        fillOpacity: 1,
                        fill: "url(#colorValue2)"
                    })
                )
            ),
            areaChartContainer
        );
    }
    
    // Update charts when theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                // Reinitialize charts with new theme colors
                setTimeout(() => {
                    if (barChartContainer) {
                        barChartContainer.innerHTML = '';
                        initCharts();
                    }
                    if (areaChartContainer) {
                        areaChartContainer.innerHTML = '';
                        initCharts();
                    }
                }, 100);
            }
        });
    });
    
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['class']
    });
}

// Reinitialize icons when needed
function reinitializeIcons() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Handle window resize for responsive behavior
window.addEventListener('resize', function() {
    // Reinitialize charts on resize if needed
    const barChartContainer = document.getElementById('barChart');
    const areaChartContainer = document.getElementById('areaChart');
    
    if (barChartContainer && barChartContainer.children.length === 0) {
        setTimeout(initCharts, 100);
    }
    if (areaChartContainer && areaChartContainer.children.length === 0) {
        setTimeout(initCharts, 100);
    }
});

