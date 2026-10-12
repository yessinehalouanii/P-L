SOURCE_CATALOG = {
    "pl": {
        "name": "P&L / Accounting",
        "description": "Financial performance by account, department, month and YTD.",
        "fields": [
            "period","account_code","account_name","department","section","category",
            "actual","budget","prior_year","ytd_actual","ytd_budget","ytd_prior_year","notes"
        ],
        "metrics": ["Revenue","Department profit","GOP","GOP margin","EBITDA","Budget variance","Prior-year variance","Expense ratios"]
    },
    "pms": {
        "name": "PMS",
        "description": "Rooms, reservations, occupancy and guest-stay operations.",
        "fields": [
            "business_date","available_rooms","rooms_sold","occupied_rooms","out_of_order_rooms",
            "complimentary_rooms","house_use_rooms","occupancy_pct","room_revenue","adr","revpar",
            "arrivals","departures","stayovers","adults","children","no_shows","cancellations","walk_ins",
            "reservation_id","guest_id","booking_date","arrival_date","departure_date","nights","room_type",
            "rate","market_segment","booking_source","channel","rate_code","company","group_code","status"
        ],
        "metrics": ["Occupancy","ADR","RevPAR","ALOS","Cancellation rate","Segment mix","Direct vs OTA","Group production","Booking pace"]
    },
    "rms": {
        "name": "RMS / Revenue System",
        "description": "Forward-looking demand, pricing, pickup and forecast data.",
        "fields": [
            "stay_date","room_type","current_rate","recommended_rate","min_rate","max_rate","forecast_occupancy",
            "forecast_rooms_sold","forecast_revenue","on_books_rooms","on_books_revenue","pickup_1d","pickup_7d",
            "demand_level","remaining_inventory","overbooking_recommendation","restriction","forecast_adr","forecast_revpar"
        ],
        "metrics": ["Forecast occupancy","Forecast ADR","Forecast RevPAR","Rate opportunity","Pickup","Pace","Forecast accuracy"]
    },
    "str": {
        "name": "STR / CoStar",
        "description": "Hotel performance against a competitive set.",
        "fields": [
            "period","hotel_occupancy","comp_occupancy","hotel_adr","comp_adr","hotel_revpar","comp_revpar",
            "occupancy_change_pct","comp_occ_change_pct","adr_change_pct","comp_adr_change_pct","revpar_change_pct",
            "comp_revpar_change_pct","mpi","ari","rgi"
        ],
        "metrics": ["MPI","ARI","RGI","Comp-set occupancy gap","Comp-set ADR gap","Comp-set RevPAR gap"]
    },
    "pos": {
        "name": "F&B POS",
        "description": "Restaurant and bar transactions, covers, checks and menu-item economics.",
        "fields": [
            "business_date","check_id","outlet","meal_period","server","table_no","open_time","close_time","covers",
            "gross_sales","discounts","complimentary","net_sales","tax","tip","payment_type","item_name","item_category",
            "quantity","item_sales","item_cost","void_flag","void_amount","waste_qty"
        ],
        "metrics": ["F&B revenue","Covers","Average cheque","Food cost %","Beverage cost %","Void %","Discount %","Menu contribution"]
    },
    "payroll": {
        "name": "Payroll / Scheduling",
        "description": "Scheduled and actual labour deployment, hours and cost.",
        "fields": [
            "employee_id","employee_name","department","position","employment_type","date","shift_start","shift_end",
            "scheduled_hours","actual_hours","regular_hours","overtime_hours","hourly_rate","regular_pay","overtime_pay",
            "total_labour_cost","absence","late","budget_hours","budget_labour_cost"
        ],
        "metrics": ["Labour cost % revenue","Hours per occupied room","Overtime","Schedule efficiency","Payroll variance","Department productivity"]
    },
    "hr": {
        "name": "HR System",
        "description": "Headcount, turnover, retention, engagement, training and people development.",
        "fields": [
            "employee_id","department","job_title","hire_date","employment_type","status","manager","termination_date",
            "termination_reason","training_status","training_completion_pct","performance_score","promotion_date","sick_days",
            "engagement_score","enps","recruitment_cost"
        ],
        "metrics": ["Headcount","Turnover","Retention","Absenteeism","Training completion","Engagement","eNPS","Recruitment cost"]
    },
    "guest": {
        "name": "Guest Feedback",
        "description": "Reviews, surveys, complaints, NPS and service-quality signals.",
        "fields": [
            "review_id","date","source","rating","guest_type","language","overall_satisfaction","nps","cleanliness_score",
            "room_score","service_score","fb_score","checkin_score","checkout_score","value_score","likelihood_return",
            "complaint_category","complaint_subcategory","complaint_opened","complaint_closed","resolution_minutes","compensation",
            "comment","sentiment"
        ],
        "metrics": ["Guest satisfaction","Online rating","NPS","Complaint rate","Resolution time","Cleanliness","Check-in","F&B satisfaction"]
    },
    "cmms": {
        "name": "Maintenance / CMMS",
        "description": "Work orders, preventive maintenance, downtime and asset risk.",
        "fields": [
            "work_order_id","opened_at","closed_at","department","location","asset_id","asset_name","problem","type","priority",
            "technician","status","labour_hours","parts_cost","labour_cost","total_cost","downtime_hours","preventive_due_date",
            "preventive_completed","repeat_failure","capex_flag"
        ],
        "metrics": ["Preventive vs reactive","Work-order SLA","Downtime","Repeat failures","Maintenance cost","Overdue PM","CapEx flags"]
    },
    "utility": {
        "name": "Utility / BMS",
        "description": "Energy, water, gas, waste and building-system consumption.",
        "fields": [
            "date","electricity_kwh","electricity_cost","gas_m3","gas_cost","water_m3","water_cost","waste_kg","waste_cost",
            "peak_demand_kw","hvac_runtime_hours","carbon_kgco2e"
        ],
        "metrics": ["Utility cost","kWh per occupied room","Water per occupied room","Waste per occupied room","Base-load variance","Carbon intensity"]
    },
    "crm": {
        "name": "CRM / Sales",
        "description": "Corporate, group and event pipeline plus account production.",
        "fields": [
            "lead_id","company","account_type","sales_manager","created_date","event_date","rooms_requested","room_revenue_estimate",
            "fb_revenue_estimate","total_opportunity","stage","probability_pct","lead_source","response_time_hours","status",
            "negotiated_rate","room_nights","ytd_revenue","prior_year_revenue","lost_reason"
        ],
        "metrics": ["Pipeline value","Lead conversion","Response time","Corporate production","Group production","Lost business","Account growth"]
    },
    "web": {
        "name": "Website / GA4 / Booking Engine",
        "description": "Digital demand, website conversion and direct-booking economics.",
        "fields": [
            "date","users","sessions","country","traffic_source","device","booking_engine_visits","booking_starts","completed_bookings",
            "booking_revenue","direct_bookings","direct_revenue","arrival_date","departure_date","rooms","nights","room_type","rate",
            "promo_code","cancelled","ad_spend","impressions","clicks"
        ],
        "metrics": ["Website conversion","Booking-engine conversion","Direct booking %","Direct revenue","ROAS","Traffic mix","Cost of acquisition"]
    },
    "consultant": {
        "name": "STEPS Consultant",
        "description": "Mystery shop, property inspection, interviews and consultant judgement.",
        "fields": [
            "assessment_id","hotel","date","consultant","engagement_type","department","checklist_item","standard","score","weight",
            "observation","severity","evidence_ref","recommendation","owner","due_date","status","photo_ref","interviewee",
            "interview_notes","mystery_shop_point","smart_action"
        ],
        "metrics": ["Mystery-shop score","Operational audit score","Priority gaps","Evidence confidence","SMART action completion","Consultant findings"]
    }
}
