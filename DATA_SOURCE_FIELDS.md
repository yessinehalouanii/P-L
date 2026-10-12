# Hotel Data Source Field Catalogue

This file lists every field supported by the meeting-demo Data Center. Hotels can provide these through CSV/XLSX exports or manual entry.

## 1. P&L / Accounting

Financial performance by account, department, month and YTD.

**Fields**

`period`, `account_code`, `account_name`, `department`, `section`, `category`, `actual`, `budget`, `prior_year`, `ytd_actual`, `ytd_budget`, `ytd_prior_year`, `notes`

**Derived/used metrics**

Revenue, Department profit, GOP, GOP margin, EBITDA, Budget variance, Prior-year variance, Expense ratios

## 2. PMS

Rooms, reservations, occupancy and guest-stay operations.

**Fields**

`business_date`, `available_rooms`, `rooms_sold`, `occupied_rooms`, `out_of_order_rooms`, `complimentary_rooms`, `house_use_rooms`, `occupancy_pct`, `room_revenue`, `adr`, `revpar`, `arrivals`, `departures`, `stayovers`, `adults`, `children`, `no_shows`, `cancellations`, `walk_ins`, `reservation_id`, `guest_id`, `booking_date`, `arrival_date`, `departure_date`, `nights`, `room_type`, `rate`, `market_segment`, `booking_source`, `channel`, `rate_code`, `company`, `group_code`, `status`

**Derived/used metrics**

Occupancy, ADR, RevPAR, ALOS, Cancellation rate, Segment mix, Direct vs OTA, Group production, Booking pace

## 3. RMS / Revenue System

Forward-looking demand, pricing, pickup and forecast data.

**Fields**

`stay_date`, `room_type`, `current_rate`, `recommended_rate`, `min_rate`, `max_rate`, `forecast_occupancy`, `forecast_rooms_sold`, `forecast_revenue`, `on_books_rooms`, `on_books_revenue`, `pickup_1d`, `pickup_7d`, `demand_level`, `remaining_inventory`, `overbooking_recommendation`, `restriction`, `forecast_adr`, `forecast_revpar`

**Derived/used metrics**

Forecast occupancy, Forecast ADR, Forecast RevPAR, Rate opportunity, Pickup, Pace, Forecast accuracy

## 4. STR / CoStar

Hotel performance against a competitive set.

**Fields**

`period`, `hotel_occupancy`, `comp_occupancy`, `hotel_adr`, `comp_adr`, `hotel_revpar`, `comp_revpar`, `occupancy_change_pct`, `comp_occ_change_pct`, `adr_change_pct`, `comp_adr_change_pct`, `revpar_change_pct`, `comp_revpar_change_pct`, `mpi`, `ari`, `rgi`

**Derived/used metrics**

MPI, ARI, RGI, Comp-set occupancy gap, Comp-set ADR gap, Comp-set RevPAR gap

## 5. F&B POS

Restaurant and bar transactions, covers, checks and menu-item economics.

**Fields**

`business_date`, `check_id`, `outlet`, `meal_period`, `server`, `table_no`, `open_time`, `close_time`, `covers`, `gross_sales`, `discounts`, `complimentary`, `net_sales`, `tax`, `tip`, `payment_type`, `item_name`, `item_category`, `quantity`, `item_sales`, `item_cost`, `void_flag`, `void_amount`, `waste_qty`

**Derived/used metrics**

F&B revenue, Covers, Average cheque, Food cost %, Beverage cost %, Void %, Discount %, Menu contribution

## 6. Payroll / Scheduling

Scheduled and actual labour deployment, hours and cost.

**Fields**

`employee_id`, `employee_name`, `department`, `position`, `employment_type`, `date`, `shift_start`, `shift_end`, `scheduled_hours`, `actual_hours`, `regular_hours`, `overtime_hours`, `hourly_rate`, `regular_pay`, `overtime_pay`, `total_labour_cost`, `absence`, `late`, `budget_hours`, `budget_labour_cost`

**Derived/used metrics**

Labour cost % revenue, Hours per occupied room, Overtime, Schedule efficiency, Payroll variance, Department productivity

## 7. HR System

Headcount, turnover, retention, engagement, training and people development.

**Fields**

`employee_id`, `department`, `job_title`, `hire_date`, `employment_type`, `status`, `manager`, `termination_date`, `termination_reason`, `training_status`, `training_completion_pct`, `performance_score`, `promotion_date`, `sick_days`, `engagement_score`, `enps`, `recruitment_cost`

**Derived/used metrics**

Headcount, Turnover, Retention, Absenteeism, Training completion, Engagement, eNPS, Recruitment cost

## 8. Guest Feedback

Reviews, surveys, complaints, NPS and service-quality signals.

**Fields**

`review_id`, `date`, `source`, `rating`, `guest_type`, `language`, `overall_satisfaction`, `nps`, `cleanliness_score`, `room_score`, `service_score`, `fb_score`, `checkin_score`, `checkout_score`, `value_score`, `likelihood_return`, `complaint_category`, `complaint_subcategory`, `complaint_opened`, `complaint_closed`, `resolution_minutes`, `compensation`, `comment`, `sentiment`

**Derived/used metrics**

Guest satisfaction, Online rating, NPS, Complaint rate, Resolution time, Cleanliness, Check-in, F&B satisfaction

## 9. Maintenance / CMMS

Work orders, preventive maintenance, downtime and asset risk.

**Fields**

`work_order_id`, `opened_at`, `closed_at`, `department`, `location`, `asset_id`, `asset_name`, `problem`, `type`, `priority`, `technician`, `status`, `labour_hours`, `parts_cost`, `labour_cost`, `total_cost`, `downtime_hours`, `preventive_due_date`, `preventive_completed`, `repeat_failure`, `capex_flag`

**Derived/used metrics**

Preventive vs reactive, Work-order SLA, Downtime, Repeat failures, Maintenance cost, Overdue PM, CapEx flags

## 10. Utility / BMS

Energy, water, gas, waste and building-system consumption.

**Fields**

`date`, `electricity_kwh`, `electricity_cost`, `gas_m3`, `gas_cost`, `water_m3`, `water_cost`, `waste_kg`, `waste_cost`, `peak_demand_kw`, `hvac_runtime_hours`, `carbon_kgco2e`

**Derived/used metrics**

Utility cost, kWh per occupied room, Water per occupied room, Waste per occupied room, Base-load variance, Carbon intensity

## 11. CRM / Sales

Corporate, group and event pipeline plus account production.

**Fields**

`lead_id`, `company`, `account_type`, `sales_manager`, `created_date`, `event_date`, `rooms_requested`, `room_revenue_estimate`, `fb_revenue_estimate`, `total_opportunity`, `stage`, `probability_pct`, `lead_source`, `response_time_hours`, `status`, `negotiated_rate`, `room_nights`, `ytd_revenue`, `prior_year_revenue`, `lost_reason`

**Derived/used metrics**

Pipeline value, Lead conversion, Response time, Corporate production, Group production, Lost business, Account growth

## 12. Website / GA4 / Booking Engine

Digital demand, website conversion and direct-booking economics.

**Fields**

`date`, `users`, `sessions`, `country`, `traffic_source`, `device`, `booking_engine_visits`, `booking_starts`, `completed_bookings`, `booking_revenue`, `direct_bookings`, `direct_revenue`, `arrival_date`, `departure_date`, `rooms`, `nights`, `room_type`, `rate`, `promo_code`, `cancelled`, `ad_spend`, `impressions`, `clicks`

**Derived/used metrics**

Website conversion, Booking-engine conversion, Direct booking %, Direct revenue, ROAS, Traffic mix, Cost of acquisition

## 13. STEPS Consultant

Mystery shop, property inspection, interviews and consultant judgement.

**Fields**

`assessment_id`, `hotel`, `date`, `consultant`, `engagement_type`, `department`, `checklist_item`, `standard`, `score`, `weight`, `observation`, `severity`, `evidence_ref`, `recommendation`, `owner`, `due_date`, `status`, `photo_ref`, `interviewee`, `interview_notes`, `mystery_shop_point`, `smart_action`

**Derived/used metrics**

Mystery-shop score, Operational audit score, Priority gaps, Evidence confidence, SMART action completion, Consultant findings
