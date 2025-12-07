import streamlit as st
import random
import time
import pandas as pd

# ==========================================
# 1. APP CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="DECA Finance Master", layout="wide", page_icon="🏙️")

# Custom CSS for the "High Finance/Terminal" Aesthetic
st.markdown("""
<style>
    /* Global Theme */
    .main {
        background-color: #0e1117;
    }
    
    /* Typography */
    .big-money {
        font-size: 2.2em;
        font-weight: 800;
        color: #00FF00; /* Terminal Green */
        font-family: 'Courier New', monospace;
        text-shadow: 0px 0px 10px rgba(0, 255, 0, 0.4);
    }
    .job-title {
        font-size: 1.4em;
        font-weight: bold;
        color: #FFD700; /* Gold */
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.9em;
        color: #888;
        text-transform: uppercase;
    }
    
    /* Performance Meters */
    .danger-zone {
        color: #FF4B4B;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        border: 1px solid #333;
        background-color: #1f2229;
        color: white;
        height: 3.5em;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #00FF00;
        color: #00FF00;
    }
    
    /* Feedback Boxes */
    .success-msg {
        padding: 20px;
        background-color: rgba(0, 255, 0, 0.05);
        border: 1px solid #00FF00;
        border-left: 5px solid #00FF00;
        margin-top: 20px;
    }
    .error-msg {
        padding: 20px;
        background-color: rgba(255, 0, 0, 0.05);
        border: 1px solid #FF4B4B;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
    .demotion-msg {
        padding: 30px;
        background-color: #2e0000;
        border: 2px solid #FF0000;
        text-align: center;
        margin-bottom: 20px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. THE DATA (50 Real Questions from your PDFs)
# ==========================================
questions_db = [
    # --- FINANCIAL ANALYSIS (FI, FM) ---
    {"category": "Financial Analysis", "question": "Which of the following is the accounting equation?", "options": ["Assets = Liabilities - Owner's Equity", "Liabilities = Owner's Equity + Assets", "Assets = Liabilities + Owner's Equity", "Owner's Equity = Assets X Liabilities"], "answer": "Assets = Liabilities + Owner's Equity", "rationale": "The accounting equation states that a business's assets are equal to its liabilities plus owner's equity. This is the foundation of the balance sheet."},
    {"category": "Financial Analysis", "question": "What is the primary purpose of a balance sheet?", "options": ["To show profit over time", "To show cash flow", "To capture financial condition at a specific moment", "To show shareholder equity changes"], "answer": "To capture financial condition at a specific moment", "rationale": "A balance sheet gives a summary of a company's financial health (Assets, Liabilities, Equity) at a specific point in time."},
    {"category": "Financial Analysis", "question": "Marginal analysis determines whether a business activity will result in:", "options": ["Marginal revenue >= Marginal cost", "Net revenue < Marginal revenue", "Marginal cost > Marginal revenue", "Sunk cost recovery"], "answer": "Marginal revenue >= Marginal cost", "rationale": "Marginal analysis compares the additional benefits of an activity to the additional costs. You proceed if benefits >= costs."},
    {"category": "Financial Analysis", "question": "A variance analysis helps a business:", "options": ["Compare with competitors", "Make choices between alternatives", "Maintain budgetary control", "Predict trends"], "answer": "Maintain budgetary control", "rationale": "Variance analysis compares actual results to the budget to identify why differences (variances) occurred."},
    {"category": "Financial Analysis", "question": "Which cost classification helps determine how well a manager performed?", "options": ["By function", "By controllability", "By behavior", "By relevance"], "answer": "By controllability", "rationale": "Controllability classifies costs based on whether a specific manager has the power to influence them."},
    {"category": "Financial Analysis", "question": "If a company pays more in dividends than it earns in net income, retained earnings will:", "options": ["Increase", "Stay the same", "Be zero", "Decrease"], "answer": "Decrease", "rationale": "Retained earnings = Beginning Earnings + Net Income - Dividends. If Dividends > Net Income, the total decreases."},
    {"category": "Financial Analysis", "question": "Cost allocation is the process of:", "options": ["Determining market price", "Assigning costs to cost objects", "Calculating taxes", "Forecasting sales"], "answer": "Assigning costs to cost objects", "rationale": "Cost allocation divides indirect costs (like rent or utilities) among different departments or products."},
    {"category": "Financial Analysis", "question": "Which represents a 'Sunk Cost'?", "options": ["Training for an employee who quit", "Raw materials", "Electric bill", "Future rent"], "answer": "Training for an employee who quit", "rationale": "Sunk costs have already been incurred and cannot be recovered. They should not influence future decisions."},
    {"category": "Financial Analysis", "question": "To calculate the future value of money, you need:", "options": ["Present value & discount rate", "Past value & principal", "Income & interest", "Past value & present value"], "answer": "Present value & discount rate", "rationale": "FV = PV * (1 + r)^n. You need the starting amount (Present Value) and the interest rate."},
    {"category": "Financial Analysis", "question": "Dividends paid to stockholders are reported on the statement of equity as:", "options": ["Additions to net income", "Subtractions from net income", "Operating expenses", "Assets"], "answer": "Subtractions from net income", "rationale": "Dividends are distributions of profit, so they reduce the Retained Earnings of the company."},

    # --- LAW, ETHICS & RISK (BL, RM) ---
    {"category": "Law & Ethics", "question": "A legally binding contract requires:", "options": ["Written signature", "Agreement by one party", "Exchange of value (consideration)", "Notarization"], "answer": "Exchange of value (consideration)", "rationale": "For a contract to be binding, something of value must be exchanged between parties."},
    {"category": "Law & Ethics", "question": "Insider trading involves:", "options": ["Buying stock in your own company", "Selling stock before a merger becomes public", "Discussing stock prices", "Analyzing public data"], "answer": "Selling stock before a merger becomes public", "rationale": "Trading based on material, non-public information is illegal insider trading."},
    {"category": "Law & Ethics", "question": "A Ponzi scheme relies on:", "options": ["Product sales", "Funds from new investors", "Government bonds", "Stock dividends"], "answer": "Funds from new investors", "rationale": "Ponzi schemes use money from new investors to pay fake 'returns' to earlier investors."},
    {"category": "Law & Ethics", "question": "Which of the following is a tax-deductible expense for a business?", "options": ["Personal vacation", "Computers for the office", "Traffic tickets", "Political contributions"], "answer": "Computers for the office", "rationale": "Necessary business equipment is tax-deductible. Personal expenses and fines are not."},
    {"category": "Law & Ethics", "question": "What is 'fiduciary responsibility'?", "options": ["Acting in the client's best interest", "Generating highest commissions", "Following manager orders", "Maximizing short-term profit"], "answer": "Acting in the client's best interest", "rationale": "A fiduciary is legally obligated to prioritize the client's financial well-being over their own."},
    {"category": "Law & Ethics", "question": "Compliance technology helps organizations primarily by:", "options": ["Improving customer service", "Reducing costs and errors", "Avoiding all regulations", "Hiring more staff"], "answer": "Reducing costs and errors", "rationale": "Automated compliance reduces the manual labor and human error associated with regulatory reporting."},
    {"category": "Law & Ethics", "question": "To manage risk, a company might form a 'captive insurance company' when:", "options": ["Commercial insurance won't cover their specific risks", "They want to avoid taxes", "They are too small for insurance", "They have no risks"], "answer": "Commercial insurance won't cover their specific risks", "rationale": "Captive insurance is a subsidiary formed to insure the parent company's specific risks."},
    {"category": "Law & Ethics", "question": "Enterprise Risk Management (ERM) involves:", "options": ["Ignoring small risks", "Identifying risks across the whole organization", "Focusing only on financial risk", "Buying insurance only"], "answer": "Identifying risks across the whole organization", "rationale": "ERM is a holistic approach to managing all types of risk (strategic, operational, financial, hazard) together."},
    {"category": "Law & Ethics", "question": "If an employee discovers a safety violation, they should:", "options": ["Ignore it", "Report it to protect employees/customers", "Fix it secretly", "Quit"], "answer": "Report it to protect employees/customers", "rationale": "Reporting noncompliance prevents accidents and protects the well-being of stakeholders."},
    {"category": "Law & Ethics", "question": "The Sarbanes-Oxley Act relates to:", "options": ["Environmental protection", "Financial record transparency", "Workplace safety", "Import tariffs"], "answer": "Financial record transparency", "rationale": "Sarbanes-Oxley (SOX) regulates financial reporting and auditing to prevent corporate fraud."},

    # --- ECONOMICS (EC) ---
    {"category": "Economics", "question": "Which economic indicator is considered 'leading' (predicts future movement)?", "options": ["Unemployment rate", "Stock market returns", "GDP", "Inflation"], "answer": "Stock market returns", "rationale": "The stock market often moves before the general economy, making it a leading indicator."},
    {"category": "Economics", "question": "During a recession (contraction), what usually decreases?", "options": ["Unemployment", "Interest rates", "Consumer spending", "Government debt"], "answer": "Consumer spending", "rationale": "In a recession, confidence drops and people spend less money."},
    {"category": "Economics", "question": "If the US Dollar weakens against the Euro, US exports to Europe become:", "options": ["More expensive", "Cheaper", "Unchanged", "Illegal"], "answer": "Cheaper", "rationale": "A weak domestic currency makes exports cheaper for foreign buyers to purchase."},
    {"category": "Economics", "question": "The law of diminishing returns states that adding more workers will eventually:", "options": ["Increase output indefinitely", "Decrease output per worker", "Eliminate costs", "Improve quality"], "answer": "Decrease output per worker", "rationale": "Adding variable resources (labor) to fixed resources (machinery) eventually yields lower marginal output."},
    {"category": "Economics", "question": "Inflation is the steady increase in:", "options": ["Stock prices", "Prices of goods and services", "Unemployment", "Savings rates"], "answer": "Prices of goods and services", "rationale": "Inflation measures the rising cost of a basket of consumer goods over time."},
    {"category": "Economics", "question": "What type of market structure involves trading unlisted stock via a dealer network?", "options": ["Auction market", "Over-the-counter (OTC)", "Futures market", "Bond market"], "answer": "Over-the-counter (OTC)", "rationale": "OTC markets handle securities not listed on major exchanges like the NYSE."},
    {"category": "Economics", "question": "Which type of unemployment is caused by a general economic downturn?", "options": ["Frictional", "Structural", "Cyclical", "Seasonal"], "answer": "Cyclical", "rationale": "Cyclical unemployment rises and falls with the business cycle (recessions/expansions)."},
    {"category": "Economics", "question": "Gross Domestic Product (GDP) measures:", "options": ["Total tax revenue", "Total value of goods/services produced", "Stock market growth", "Consumer debt"], "answer": "Total value of goods/services produced", "rationale": "GDP is the standard measure of a country's total economic output."},
    {"category": "Economics", "question": "When supply exceeds demand, prices tend to:", "options": ["Increase", "Decrease", "Stay the same", "Fluctuate wildly"], "answer": "Decrease", "rationale": "Surplus supply puts downward pressure on prices to clear the market."},
    {"category": "Economics", "question": "A tax on imported goods is called a:", "options": ["Quota", "Subsidy", "Tariff", "Embargo"], "answer": "Tariff", "rationale": "Tariffs are taxes levied on imports to protect domestic industries or raise revenue."},

    # --- SYSTEMS & DATA (NF, OP, SM) ---
    {"category": "Systems & Data", "question": "Data cleansing is used to:", "options": ["Encrypt data", "Remove errors and duplicates", "Speed up internet", "Monitor employees"], "answer": "Remove errors and duplicates", "rationale": "Data cleansing ensures databases are accurate, consistent, and useful for analysis."},
    {"category": "Systems & Data", "question": "What allows businesses to share information between different computer systems?", "options": ["Electronic Data Interchange (EDI)", "Word Processing", "Spreadsheets", "Flash drives"], "answer": "Electronic Data Interchange (EDI)", "rationale": "EDI is the standard format for exchanging business data between different companies' systems."},
    {"category": "Systems & Data", "question": "Predictive analytics uses data to:", "options": ["Summarize the past", "Forecast future events", "Clean databases", "Audit taxes"], "answer": "Forecast future events", "rationale": "Predictive analytics uses historical data to model probable future outcomes."},
    {"category": "Systems & Data", "question": "A central data repository ensures:", "options": ["Slower access", "Inconsistent data", "Up-to-date, consistent data", "Data isolation"], "answer": "Up-to-date, consistent data", "rationale": "Central repositories provide a 'single source of truth' for the entire organization."},
    {"category": "Systems & Data", "question": "Tokenization protects online transactions by:", "options": ["Lowering prices", "Substituting data with a random symbol", "Increasing speed", "Removing taxes"], "answer": "Substituting data with a random symbol", "rationale": "Tokenization replaces sensitive data (like card numbers) with a useless 'token' to prevent theft."},
    {"category": "Systems & Data", "question": "What is the first step in project planning?", "options": ["Identify stakeholders", "Determine budget", "Schedule tasks", "Evaluate results"], "answer": "Identify stakeholders", "rationale": "You must know who is involved and what they need before defining scope or budget."},
    {"category": "Systems & Data", "question": "Lean operations focus on:", "options": ["Increasing waste", "Eliminating waste", "Increasing inventory", "Reducing quality"], "answer": "Eliminating waste", "rationale": "Lean methodology aims to maximize value by removing all non-value-added activities (waste)."},
    {"category": "Systems & Data", "question": "The 'Critical Path' in project management represents:", "options": ["The shortest time to complete", "The longest path of planned activities", "The most expensive tasks", "The easiest tasks"], "answer": "The longest path of planned activities", "rationale": "The critical path determines the earliest possible end date; if a critical task slips, the project slips."},
    {"category": "Systems & Data", "question": "Encryption protects data by:", "options": ["Deleting it", "Transforming it into secret code", "Backing it up", "Organizing it"], "answer": "Transforming it into secret code", "rationale": "Encryption makes data unreadable to unauthorized users without a decryption key."},
    {"category": "Systems & Data", "question": "A 'dashboard' in finance is used to:", "options": ["Drive cars", "Visualize key performance indicators (KPIs)", "Write code", "File taxes"], "answer": "Visualize key performance indicators (KPIs)", "rationale": "Dashboards provide at-a-glance views of critical data metrics."},

    # --- SOFT SKILLS (CO, CR, EI, HR, PD) ---
    {"category": "Soft Skills", "question": "Initiative is defined as:", "options": ["Waiting for instructions", "Acting without being told", "Doing the bare minimum", "Asking for help constantly"], "answer": "Acting without being told", "rationale": "Initiative involves recognizing what needs to be done and doing it proactively."},
    {"category": "Soft Skills", "question": "Active listening involves:", "options": ["Interrupting to ask questions", "Thinking about your reply", "Verbal acknowledgment and eye contact", "Multitasking"], "answer": "Verbal acknowledgment and eye contact", "rationale": "Active listening requires full attention and providing feedback (nodding, 'I see') to the speaker."},
    {"category": "Soft Skills", "question": "To build trust with a client, a finance professional should:", "options": ["Hide risks", "Be transparent and honest", "Use complex jargon", "Guarantee returns"], "answer": "Be transparent and honest", "rationale": "Transparency builds long-term trust. Hiding risks or guaranteeing returns is unethical."},
    {"category": "Soft Skills", "question": "When negotiating, 'Batna' stands for:", "options": ["Best Alternative to a Negotiated Agreement", "Better Ask The New Associate", "Business Assets To Net Assets", "Buy All The New Assets"], "answer": "Best Alternative to a Negotiated Agreement", "rationale": "BATNA is your backup plan if negotiations fail; knowing it gives you leverage."},
    {"category": "Soft Skills", "question": "A 'Whistleblower' policy encourages employees to:", "options": ["Spy on coworkers", "Report unethical behavior without fear", "Gossip", "Leak secrets to competitors"], "answer": "Report unethical behavior without fear", "rationale": "Whistleblower protections ensure employees can report illegal acts without retaliation."},
    {"category": "Soft Skills", "question": "Emotional Intelligence (EQ) includes:", "options": ["IQ score", "Self-awareness and empathy", "Math skills", "Memorization"], "answer": "Self-awareness and empathy", "rationale": "EQ is the ability to understand and manage your own emotions and those of others."},
    {"category": "Soft Skills", "question": "In a job interview, 'Tell me about yourself' is a test of:", "options": ["Your life story", "Communication skills and professional summary", "Honesty", "Your hobbies"], "answer": "Communication skills and professional summary", "rationale": "Interviewers want a concise summary of your professional background and relevance to the role."},
    {"category": "Soft Skills", "question": "Consensus building means:", "options": ["Voting", "Majority rule", "Reaching substantial agreement", "The leader decides"], "answer": "Reaching substantial agreement", "rationale": "Consensus means the group generally agrees and can support the decision, even if not everyone loves it."},
    {"category": "Soft Skills", "question": "Which communication channel is best for sensitive bad news?", "options": ["Email", "Text message", "Face-to-face", "Memo"], "answer": "Face-to-face", "rationale": "Sensitive news requires reading non-verbal cues and showing empathy, best done in person."},
    {"category": "Soft Skills", "question": "Networking is primarily about:", "options": ["Asking for jobs", "Building mutually beneficial relationships", "Collecting business cards", "Selling products"], "answer": "Building mutually beneficial relationships", "rationale": "Effective networking is about exchange and relationship building, not just taking."},
]

# ==========================================
# 3. GAME LOGIC & STATE MANAGEMENT
# ==========================================

# --- A. Initialize Variables ---
if 'balance' not in st.session_state:
    st.session_state.balance = 0            # Liquid Cash (Spendable)
if 'lifetime_earnings' not in st.session_state:
    st.session_state.lifetime_earnings = 0  # Career Score (For Title)
if 'office_level' not in st.session_state:
    st.session_state.office_level = "The Basement"
if 'staff' not in st.session_state:
    st.session_state.staff = []             # List of hired help
if 'performance_history' not in st.session_state:
    st.session_state.performance_history = [] # Rolling window of last 20 answers (True/False)
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'last_result' not in st.session_state:
    st.session_state.last_result = None     # "Correct", "Incorrect", "Demoted"
if 'eliminated_options' not in st.session_state:
    st.session_state.eliminated_options = []

# --- B. Career Logic (The Ladder) ---
def get_title(earnings):
    if earnings < 50000: return "Unpaid Intern"
    elif earnings < 150000: return "Junior Analyst"
    elif earnings < 500000: return "Associate"
    elif earnings < 2000000: return "Vice President"
    elif earnings < 10000000: return "Managing Director"
    else: return "Master of the Universe"

# --- C. Asset Data ---
office_tiers = {
    "The Basement": {"cost": 0, "img": "https://images.unsplash.com/photo-1504384308090-c54be3855833?w=400"},
    "The Bullpen": {"cost": 50000, "img": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=400"},
    "Associate Office": {"cost": 200000, "img": "https://images.unsplash.com/photo-1662973599908-724d27ae3443?w=400"},
    "VP Suite": {"cost": 1000000, "img": "https://images.unsplash.com/photo-1600607686527-6fb886090705?w=400"},
    "The Penthouse": {"cost": 10000000, "img": "https://images.unsplash.com/photo-1512918760383-5658fc14bc63?w=400"}
}

talent_roster = {
    "Junior Analyst": {"cost": 20000, "desc": "Unlocks 'Research Note' (Hints)", "icon": "💡"},
    "The Quant": {"cost": 75000, "desc": "Unlocks 'Algorithm' (Eliminate 2 wrong)", "icon": "📉"},
    "Risk Manager": {"cost": 150000, "desc": "Unlocks 'Hedge' (Skip question)", "icon": "🛡️"}
}

# --- D. Core Functions ---

def new_question(category="All"):
    st.session_state.last_result = None
    st.session_state.eliminated_options = []
    
    if category == "All":
        # Weighting: prioritize areas where user is weak could be V2.
        st.session_state.current_question = random.choice(questions_db)
    else:
        filtered = [q for q in questions_db if q['category'] == category]
        if filtered:
            st.session_state.current_question = random.choice(filtered)
        else:
            st.error("No data for this sector. Sourcing globally.")
            st.session_state.current_question = random.choice(questions_db)

def check_answer(user_ans):
    correct_ans = st.session_state.current_question['answer']
    
    if user_ans == correct_ans:
        # Success Logic
        payout = 10000
        st.session_state.balance += payout
        st.session_state.lifetime_earnings += payout
        st.session_state.last_result = "Correct"
        st.session_state.performance_history.append(True)
    else:
        # Failure Logic
        st.session_state.last_result = "Incorrect"
        st.session_state.performance_history.append(False)
    
    # Feature 6: Risk of Ruin Protocol
    check_risk_of_ruin()

def check_risk_of_ruin():
    # Only check if we have enough history
    history = st.session_state.performance_history
    if len(history) > 20:
        # Keep window at 20
        st.session_state.performance_history = history[-20:]
        history = st.session_state.performance_history
        
    if len(history) == 20:
        accuracy = sum(history) / len(history)
        if accuracy < 0.70: # Survival Threshold
            execute_demotion()

def execute_demotion():
    # Feature 6 Implementation
    st.session_state.last_result = "Demoted"
    
    # 1. Title Strip (Slash lifetime earnings effectively demoting title)
    # We set them back to the start of the previous tier
    current_earnings = st.session_state.lifetime_earnings
    if current_earnings > 2000000: st.session_state.lifetime_earnings = 500000
    elif current_earnings > 500000: st.session_state.lifetime_earnings = 150000
    elif current_earnings > 150000: st.session_state.lifetime_earnings = 50000
    else: st.session_state.lifetime_earnings = 0
    
    # 2. Asset Seizure (Office Foreclosure)
    st.session_state.office_level = "The Basement"
    
    # 3. Staff Layoffs (Optional, but ruthless)
    st.session_state.staff = []
    
    # 4. Reset Performance History (Give them a clean slate to rebuild)
    st.session_state.performance_history = []

def use_quant():
    q = st.session_state.current_question
    # Find wrong options
    wrong_options = [opt for opt in q['options'] if opt != q['answer']]
    # Pick 2 to kill
    if len(wrong_options) >= 2:
        to_eliminate = random.sample(wrong_options, 2)
        st.session_state.eliminated_options = to_eliminate

# ==========================================
# 4. SIDEBAR (THE DASHBOARD)
# ==========================================
with st.sidebar:
    st.markdown("## 🏛️ DECA CAPITAL")
    
    # 1. Career Status
    current_title = get_title(st.session_state.lifetime_earnings)
    st.markdown(f"**ROLE:**")
    st.markdown(f'<div class="job-title">{current_title}</div>', unsafe_allow_html=True)
    
    # 2. Financials
    st.markdown("**LIQUIDITY (Spendable):**")
    st.markdown(f'<div class="big-money">${st.session_state.balance:,.0f}</div>', unsafe_allow_html=True)
    
    st.caption(f"Lifetime Volume: ${st.session_state.lifetime_earnings:,.0f}")
    
    st.markdown("---")
    
    # 3. Assets
    st.markdown(f"**HQ:** {st.session_state.office_level}")
    
    # 4. Performance (The Risk Monitor)
    history = st.session_state.performance_history
    if len(history) > 0:
        acc = sum(history) / len(history)
        st.write(f"**Rolling Accuracy (Last 20):** {acc*100:.0f}%")
        st.progress(acc)
        if acc < 0.75 and len(history) > 10:
            st.markdown('<p class="danger-zone">⚠️ RISK OF RUIN IMMINENT</p>', unsafe_allow_html=True)
    else:
        st.write("Performance: No data yet")

# ==========================================
# 5. MAIN INTERFACE
# ==========================================

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["⚡ TRADING FLOOR (Quiz)", "🏢 REAL ESTATE", "🤝 HEADHUNTER"])

# --- TAB 1: THE TRADING FLOOR ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Market Operations")
    with col2:
        # Category Selector
        category = st.selectbox("Market Sector", ["All", "Financial Analysis", "Law & Ethics", "Economics", "Systems & Data", "Soft Skills"])

    # If no question is active, show Start Button
    if st.session_state.current_question is None:
        st.info("Market is open. Initiate trading sequence.")
        if st.button("INITIATE DEAL FLOW"):
            new_question(category)
            st.rerun()

    # Active Question Display
    else:
        q = st.session_state.current_question
        
        # Display Question Area
        st.markdown(f"**SECTOR: {q['category'].upper()}**")
        st.markdown(f"### {q['question']}")
        
        st.markdown("---")

        # LIFELINES (Talent Acquisition) - Only show if hired and not yet answered
        if st.session_state.last_result is None:
            ll_col1, ll_col2, ll_col3 = st.columns(3)
            
            # 1. Junior Analyst (Hint)
            with ll_col1:
                if "Junior Analyst" in st.session_state.staff:
                    if st.button("💡 Analyst Note"):
                        st.info(f"**INTERNAL MEMO:** {q['rationale']}")
                else:
                    st.caption("🔒 Hire Analyst to unlock Hints")

            # 2. The Quant (50/50)
            with ll_col2:
                if "The Quant" in st.session_state.staff:
                    if st.button("📉 Quant Algo"):
                        use_quant()
                        st.rerun()
                else:
                    st.caption("🔒 Hire Quant to unlock 50/50")

            # 3. Risk Manager (Skip)
            with ll_col3:
                if "Risk Manager" in st.session_state.staff:
                    if st.button("🛡️ Hedge Position"):
                        new_question(category)
                        st.rerun()
                else:
                    st.caption("🔒 Hire Risk Manager to Skip")

        # Answer Options Display
        options = q['options']
        col_a, col_b = st.columns(2)
        
        for i, option in enumerate(options):
            # Check if option was eliminated by Quant
            is_disabled = option in st.session_state.eliminated_options
            # Check if question is already answered (disable all)
            is_answered = st.session_state.last_result is not None
            
            label = option
            if is_disabled:
                label = f"❌ {option}"
            
            # Layout logic
            target_col = col_a if i % 2 == 0 else col_b
            
            with target_col:
                if st.button(label, key=option, disabled=is_disabled or is_answered):
                    check_answer(option)
                    st.rerun()

        # RESULT NOTIFICATIONS
        if st.session_state.last_result == "Correct":
            st.markdown(f"""
            <div class="success-msg">
                <h3>✅ DEAL CLOSED. WIRE RECEIVED.</h3>
                <p><strong>+$10,000</strong> has been deposited to your account.</p>
                <p><em>Market Insight: {q['rationale']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SOURCE NEXT DEAL ->", type="primary"):
                new_question(category)
                st.rerun()

        elif st.session_state.last_result == "Incorrect":
            st.markdown(f"""
            <div class="error-msg">
                <h3>❌ DEAL FAILED. LOSS INCURRED.</h3>
                <p>The winning move was: <strong>{q['answer']}</strong></p>
                <p><em>Market Insight: {q['rationale']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("RE-EVALUATE MARKET (Next) ->"):
                new_question(category)
                st.rerun()

        elif st.session_state.last_result == "Demoted":
            st.markdown("""
            <div class="demotion-msg">
                <h1>📉 MARGIN CALL: ASSETS SEIZED</h1>
                <p>Your performance dropped below the survival threshold (70%).</p>
                <p><strong>CONSEQUENCES:</strong></p>
                <ul>
                    <li>Job Title Stripped</li>
                    <li>Office Foreclosed (Returned to Basement)</li>
                    <li>Staff Laid Off</li>
                </ul>
                <p>You must rebuild from the bottom.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("BEGIN RECOVERY ->", type="primary"):
                st.session_state.last_result = None
                new_question(category)
                st.rerun()

# --- TAB 2: VISUAL EMPIRE ---
with tab2:
    st.header("Real Estate Portfolio")
    st.write("Upgrade your environment to reflect your status.")
    
    # Display Grid
    c1, c2 = st.columns(2)
    
    # Helper to display card
    def show_office_card(col, name, cost, img_url):
        with col:
            st.image(img_url, use_column_width=True)
            st.subheader(name)
            st.write(f"**Price:** ${cost:,.0f}")
            
            if st.session_state.office_level == name:
                st.button("✅ CURRENT HQ", key=f"btn_{name}", disabled=True)
            else:
                if st.button(f"Acquire {name}", key=f"btn_{name}"):
                    if st.session_state.balance >= cost:
                        st.session_state.balance -= cost
                        st.session_state.office_level = name
                        st.success(f"Move-in complete! Welcome to {name}.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Insufficient Capital. Need ${cost - st.session_state.balance:,.0f} more.")
            st.divider()

    # Render Items
    items = list(office_tiers.items())
    for i, (name, data) in enumerate(items):
        target_col = c1 if i % 2 == 0 else c2
        show_office_card(target_col, name, data['cost'], data['img'])

# --- TAB 3: HEADHUNTER ---
with tab3:
    st.header("Talent Acquisition")
    st.write("Leverage human capital to mitigate risk and improve accuracy.")
    
    for role, info in talent_roster.items():
        with st.container():
            col_icon, col_desc, col_action = st.columns([1, 3, 1])
            
            with col_icon:
                st.markdown(f"<h1 style='text-align: center;'>{info['icon']}</h1>", unsafe_allow_html=True)
            
            with col_desc:
                st.subheader(role)
                st.write(info['desc'])
                st.caption(f"Signing Bonus: ${info['cost']:,.0f}")
                
            with col_action:
                st.write("") # Spacer
                if role in st.session_state.staff:
                    st.button("ON PAYROLL", key=f"hire_{role}", disabled=True)
                else:
                    if st.button(f"HIRE", key=f"hire_{role}"):
                        if st.session_state.balance >= info['cost']:
                            st.session_state.balance -= info['cost']
                            st.session_state.staff.append(role)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Insufficient Funds")
            st.divider()
