// Global variables
let analysisData = null;
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    checkAuth();
    loadUserInfo();
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const analyzeUserBtn = document.getElementById('analyzeUserBtn');
    
    if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeInfluencers);
    if (refreshBtn) refreshBtn.addEventListener('click', refreshData);
    if (analyzeUserBtn) analyzeUserBtn.addEventListener('click', searchInfluencer);
    
    // Add enter key support for search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchInfluencer();
            }
        });
    }
});

function checkAuth() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn || isLoggedIn !== 'true') {
        window.location.href = '/';
    }
}

function loadUserInfo() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    
    if (currentUser.fullName) {
        const userNameEl = document.getElementById('userName');
        const userEmailEl = document.getElementById('userEmail');
        const userAvatarEl = document.getElementById('userAvatar');
        
        if (userNameEl) userNameEl.textContent = currentUser.fullName;
        if (userEmailEl) userEmailEl.textContent = currentUser.email;
        
        // Set avatar initial
        if (userAvatarEl) {
            const initial = currentUser.fullName.charAt(0).toUpperCase();
            userAvatarEl.textContent = initial;
        }
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('currentUser');
        localStorage.removeItem('isLoggedIn');
        window.location.href = '/';
    }
}

function viewProfile() {
    window.location.href = '/profile';
}

// Search influencer functionality
async function searchInfluencer() {
    const username = document.getElementById('searchInput').value.trim();
    
    if (!username) {
        alert('Please enter an Instagram username');
        return;
    }
    
    showLoading();
    
    try {
        // Simulated search - in your case, load from sample data
        const sampleInfluencers = [
            'ViratKohli',
            'PriyankaChopra',
            'AliaBhatt',
            'ShraddhaKapoor',
            'DeepikaPadukone',
            'NehaKakkar'
        ];
        
        // Check if influencer exists in sample data
        const normalizedUsername = username.toLowerCase();
        const found = sampleInfluencers.some(inf => inf.toLowerCase() === normalizedUsername);
        
        if (!found) {
            hideLoading();
            alert('Influencer "' + username + '" not found in database. Try: ' + sampleInfluencers.join(', '));
            return;
        }
        
        // Load data for this influencer
        const response = await fetch('/api/influencer/' + username);
        const data = await response.json();
        
        if (data.status === 'error') {
            alert(data.message || 'Influencer not found');
            hideLoading();
            return;
        }
        
        displaySearchResults(data, username);
        await loadBrandRecommendations(username, data);
        hideLoading();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to search influencer. Make sure to click "Analyze All Influencers" first.');
        hideLoading();
    }
}

function displaySearchResults(data, username) {
    const resultsDiv = document.getElementById('searchResults');
    
    const metrics = data.metrics.influencer_metrics[0] || {};
    const credibility = data.credibility.credibility_analysis[0] || {};
    const sentiment = data.sentiment.sentiment_analysis[0] || {};
    
    const initial = username.charAt(0).toUpperCase();
    
    // Calculate follower statistics
    const totalFollowers = credibility.total_followers || 50000;
    const fakeFollowers = credibility.estimated_fake_followers || 0;
    const realFollowers = credibility.estimated_real_followers || totalFollowers;
    const fakePercentage = credibility.fake_percentage || 0;
    const authenticityCategory = credibility.authenticity_category || 'Good';
    const authenticityIcon = credibility.authenticity_icon || '🟢';
    
    resultsDiv.innerHTML = `
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">${initial}</div>
                <div>
                    <h2>@${username}</h2>
                    <p style="color: #666;">Influencer Profile</p>
                </div>
            </div>
            
            <!-- Follower Statistics Section -->
            <div style="background: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #667eea; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                    👥 Follower Analysis
                    <span style="font-size: 1.5em;">${authenticityIcon}</span>
                    <span style="font-size: 0.8em; color: #666;">${authenticityCategory}</span>
                </h3>
                
                <div class="follower-stats-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px;">
                    <div class="follower-stat-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 8px;">Total Followers</div>
                        <div style="font-size: 2.2em; font-weight: bold;">${formatNumber(totalFollowers)}</div>
                    </div>
                    
                    <div class="follower-stat-box" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 8px;">Real Followers</div>
                        <div style="font-size: 2.2em; font-weight: bold;">${formatNumber(realFollowers)}</div>
                        <div style="font-size: 0.85em; margin-top: 5px; opacity: 0.9;">${(100 - fakePercentage).toFixed(1)}% Authentic</div>
                    </div>
                    
                    <div class="follower-stat-box" style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 20px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 8px;">Fake Followers</div>
                        <div style="font-size: 2.2em; font-weight: bold;">${formatNumber(fakeFollowers)}</div>
                        <div style="font-size: 0.85em; margin-top: 5px; opacity: 0.9;">${fakePercentage.toFixed(1)}% Suspicious</div>
                    </div>
                    
                    <div class="follower-stat-box" style="background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%); color: white; padding: 20px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 8px;">Follower Quality</div>
                        <div style="font-size: 2.2em; font-weight: bold;">${(credibility.follower_quality * 100).toFixed(0)}%</div>
                        <div style="font-size: 0.85em; margin-top: 5px; opacity: 0.9;">Ratio: ${credibility.follower_ratio || '1:1'}</div>
                    </div>
                </div>
                
                <!-- Follower Authenticity Bar -->
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-weight: 600; color: #333;">Follower Authenticity</span>
                        <span style="font-weight: 600; color: #667eea;">${(100 - fakePercentage).toFixed(1)}% Real</span>
                    </div>
                    <div style="background: #e0e0e0; height: 30px; border-radius: 15px; overflow: hidden; position: relative;">
                        <div style="background: linear-gradient(90deg, #28a745, #20c997); height: 100%; width: ${100 - fakePercentage}%; transition: width 0.3s ease;"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: bold; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                            ${(100 - fakePercentage).toFixed(1)}% Authentic
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.85em; color: #666;">
                        <span>🟢 Real: ${formatNumber(realFollowers)}</span>
                        <span>🔴 Fake: ${formatNumber(fakeFollowers)}</span>
                    </div>
                </div>
                
                <!-- Detection Indicators -->
                <div style="margin-top: 20px; display: grid; gap: 10px;">
                    <div style="display: flex; justify-content: space-between; padding: 12px; background: #f8f9fa; border-radius: 8px;">
                        <span style="color: #666;">Engagement Authenticity:</span>
                        <span style="font-weight: bold; color: ${credibility.engagement_authenticity > 0.7 ? '#28a745' : credibility.engagement_authenticity > 0.5 ? '#ffc107' : '#dc3545'};">
                            ${((credibility.engagement_authenticity || 0.8) * 100).toFixed(0)}%
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px; background: #f8f9fa; border-radius: 8px;">
                        <span style="color: #666;">Like to Follower Ratio:</span>
                        <span style="font-weight: bold; color: #667eea;">
                            ${credibility.like_ratio || '2.5'}%
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px; background: #f8f9fa; border-radius: 8px;">
                        <span style="color: #666;">Comment to Like Ratio:</span>
                        <span style="font-weight: bold; color: #667eea;">
                            ${credibility.comment_ratio || '0.8'}%
                        </span>
                    </div>
                    ${credibility.spike_detected ? `
                    <div style="padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 8px;">
                        <strong style="color: #856404;">⚠️ Unusual Activity Detected</strong>
                        <p style="margin: 5px 0 0 0; color: #856404; font-size: 0.9em;">Suspicious engagement spikes detected in recent posts</p>
                    </div>
                    ` : ''}
                </div>
            </div>
            
            <div class="profile-stats">
                <div class="stat-box">
                    <h4>${formatNumber(metrics.total_likes || 0)}</h4>
                    <p>Total Likes</p>
                </div>
                <div class="stat-box">
                    <h4>${formatNumber(metrics.total_comments || 0)}</h4>
                    <p>Total Comments</p>
                </div>
                <div class="stat-box">
                    <h4>${metrics.avg_reach ? metrics.avg_reach.toFixed(0) : 0}</h4>
                    <p>Avg Reach</p>
                </div>
            </div>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <h3>Engagement Rate</h3>
                <p class="metric">${metrics.engagement_rate || 0}%</p>
            </div>
            <div class="card">
                <h3>Consistency</h3>
                <p class="metric">${metrics.consistency_score || 0}</p>
            </div>
            <div class="card">
                <h3>Credibility Score</h3>
                <p class="metric">${((credibility.credibility_score || 0) * 100).toFixed(1)}%</p>
            </div>
            <div class="card">
                <h3>Sentiment</h3>
                <p class="metric">${sentiment.comment_sentiment || 'Neutral'}</p>
            </div>
        </div>
        
        <div id="brandRecommendations"></div>
    `;
    
    resultsDiv.style.display = 'block';
}

async function loadBrandRecommendations(username, data) {
    try {
        const metrics = data.metrics.influencer_metrics[0] || {};
        const credibility = data.credibility.credibility_analysis[0] || {};
        
        // Detect niche from username
        let niche = 'Lifestyle';
        if (username.toLowerCase().includes('fashion')) niche = 'Fashion';
        else if (username.toLowerCase().includes('tech')) niche = 'Tech';
        else if (username.toLowerCase().includes('fitness')) niche = 'Fitness';
        else if (username.toLowerCase().includes('travel')) niche = 'Travel';
        else if (username.toLowerCase().includes('food')) niche = 'Food';
        
        const recommendations = {
            influencer_name: username,
            niche: niche,
            audience_demographics: {
                age_groups: {'18-24': 35, '25-34': 40, '35-44': 20, '45+': 5},
                gender: {'Female': 55, 'Male': 45},
                top_countries: ['India', 'USA', 'UAE'],
                interests: ['Fashion', 'Lifestyle', 'Entertainment']
            },
            recommended_brands: getBrandsByNiche(niche),
            collaboration_types: [
                {type: 'Sponsored Post', description: 'Single post featuring brand', suitability_score: 0.85},
                {type: 'Product Review', description: 'Detailed review', suitability_score: 0.75},
                {type: 'Reel Promotion', description: 'Short video content', suitability_score: 0.90}
            ],
            estimated_price_range: {
                min_price: 15000,
                max_price: 45000,
                currency: 'INR'
            },
            metrics_summary: {
                followers: credibility.total_followers || 50000,
                real_followers: credibility.estimated_real_followers || 45000,
                fake_followers: credibility.estimated_fake_followers || 5000,
                engagement_rate: metrics.engagement_rate || 0,
                credibility_score: credibility.credibility_score || 0.5,
                credibility_status: credibility.credibility_status || 'Medium'
            }
        };
        
        displayBrandRecommendations(recommendations);
        
    } catch (error) {
        console.error('Error loading brand recommendations:', error);
    }
}

function getBrandsByNiche(niche) {
    const brandDatabase = {
        'Fashion': ['Zara', 'H&M', 'Myntra', 'Forever 21', 'Mango', 'Urbanic', 'Shein', 'Ajio'],
        'Tech': ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Realme', 'Amazon', 'Flipkart', 'Google'],
        'Fitness': ['Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour', 'Decathlon', 'Cult.fit', 'HealthifyMe'],
        'Travel': ['MakeMyTrip', 'Airbnb', 'Booking.com', 'TripAdvisor', 'OYO', 'Cleartrip', 'Goibibo', 'Yatra'],
        'Food': ['Swiggy', 'Zomato', 'Dominos', 'McDonalds', 'KFC', 'Starbucks', 'Dunkin', 'Blinkit'],
        'Lifestyle': ['Amazon', 'Flipkart', 'Urban Ladder', 'Pepperfry', 'IKEA', 'Fabindia', 'Westside', 'Shoppers Stop']
    };
    
    return brandDatabase[niche] || brandDatabase['Lifestyle'];
}

function displayBrandRecommendations(rec) {
    const recDiv = document.getElementById('brandRecommendations');
    
    if (!rec) {
        recDiv.innerHTML = '<p>Brand recommendations not available</p>';
        return;
    }
    
    const priceRange = rec.estimated_price_range;
    
    recDiv.innerHTML = `
        <div class="recommendations-section">
            <h2 style="text-align: center; color: #667eea; margin-bottom: 30px;">
                🤖 AI-Powered Brand Collaboration Recommendations
            </h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>📌 Influencer Niche: <span style="color: #667eea;">${rec.niche}</span></h3>
                <div style="margin-top: 15px;">
                    <strong>Audience Demographics:</strong>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
                        <div><strong>Age Groups:</strong> ${Object.entries(rec.audience_demographics.age_groups).map(([age, pct]) => `${age}: ${pct}%`).join(', ')}</div>
                        <div><strong>Gender:</strong> ${Object.entries(rec.audience_demographics.gender).map(([g, pct]) => `${g}: ${pct}%`).join(', ')}</div>
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Top Countries:</strong> ${rec.audience_demographics.top_countries.join(', ')}
                    </div>
                </div>
            </div>
            
            <h3>🎯 Recommended Brands</h3>
            <div class="brand-grid">
                ${rec.recommended_brands.map(brand => `
                    <div class="brand-card">
                        ${brand}
                    </div>
                `).join('')}
            </div>
            
            <h3 style="margin-top: 30px;">💼 Ideal Collaboration Types</h3>
            <div class="collab-types">
                ${rec.collaboration_types.map((collab, idx) => `
                    <div class="collab-item">
                        <h4>${idx + 1}. ${collab.type}</h4>
                        <p style="color: #666; margin: 10px 0;">${collab.description}</p>
                        <p><strong>Suitability Score:</strong> 
                            <span style="color: #667eea;">${(collab.suitability_score * 100).toFixed(0)}%</span>
                        </p>
                    </div>
                `).join('')}
            </div>
            
            <div class="price-range">
                <h3>💰 Estimated Collaboration Price Range</h3>
                <h2>₹${formatNumber(priceRange.min_price)} - ₹${formatNumber(priceRange.max_price)}</h2>
                <p style="opacity: 0.9;">Per Post / Collaboration</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3>📊 Metrics Summary</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px;">
                    <div>
                        <strong>Total Followers:</strong> ${formatNumber(rec.metrics_summary.followers)}
                    </div>
                    <div>
                        <strong>Real Followers:</strong> ${formatNumber(rec.metrics_summary.real_followers)}
                    </div>
                    <div>
                        <strong>Fake Followers:</strong> ${formatNumber(rec.metrics_summary.fake_followers)}
                    </div>
                    <div>
                        <strong>Engagement Rate:</strong> ${rec.metrics_summary.engagement_rate}%
                    </div>
                    <div>
                        <strong>Credibility:</strong> ${(rec.metrics_summary.credibility_score * 100).toFixed(1)}%
                    </div>
                    <div>
                        <strong>Status:</strong> 
                        <span class="status-${rec.metrics_summary.credibility_status.toLowerCase()}">
                            ${rec.metrics_summary.credibility_status}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num;
}

async function analyzeInfluencers() {
    showLoading();
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            analysisData = data;
            displayDashboard(data);
        } else {
            alert('Error analyzing data: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze data. Please try again.');
    } finally {
        hideLoading();
    }
}

async function refreshData() {
    location.reload();
}

function showLoading() {
    const loading = document.getElementById('loading');
    const dashboard = document.getElementById('dashboard');
    if (loading) loading.classList.remove('hidden');
    if (dashboard) dashboard.classList.add('hidden');
}

function hideLoading() {
    const loading = document.getElementById('loading');
    const dashboard = document.getElementById('dashboard');
    if (loading) loading.classList.add('hidden');
    if (dashboard) dashboard.classList.remove('hidden');
}

function displayDashboard(data) {
    updateSummaryCards(data);
    createEngagementChart(data.metrics);
    createCredibilityChart(data.credibility);
    createSentimentChart(data.sentiment);
    createReachChart(data.metrics);
    createFollowerChart(data.credibility);
    createInfluencerTable(data);
}

function updateSummaryCards(data) {
    const totalInfluencers = document.getElementById('totalInfluencers');
    const avgEngagement = document.getElementById('avgEngagement');
    const avgCredibility = document.getElementById('avgCredibility');
    const avgSentiment = document.getElementById('avgSentiment');
    
    if (totalInfluencers) totalInfluencers.textContent = data.metrics.summary.total_influencers;
    if (avgEngagement) avgEngagement.textContent = data.metrics.summary.avg_engagement_rate + '%';
    if (avgCredibility) avgCredibility.textContent = (data.credibility.summary.avg_credibility * 100).toFixed(1) + '%';
    if (avgSentiment) avgSentiment.textContent = data.sentiment.summary.avg_comment_polarity.toFixed(2);
}

function createFollowerChart(credibilityData) {
    const canvas = document.getElementById('followerChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.follower) {
        charts.follower.destroy();
    }
    
    const influencers = credibilityData.credibility_analysis.map(c => c.influencer_name);
    const realFollowers = credibilityData.credibility_analysis.map(c => c.real_percentage || 80);
    const fakeFollowers = credibilityData.credibility_analysis.map(c => c.fake_percentage || 20);
    
    charts.follower = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: influencers,
            datasets: [
                {
                    label: 'Real Followers (%)',
                    data: realFollowers,
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Fake Followers (%)',
                    data: fakeFollowers,
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    });
}

function createSentimentChart(sentimentData) {
    const canvas = document.getElementById('sentimentChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.sentiment) {
        charts.sentiment.destroy();
    }
    
    const influencers = sentimentData.sentiment_analysis.map(s => s.influencer_name);
    const positiveComments = sentimentData.sentiment_analysis.map(s => s.positive_comments_pct);
    const negativeComments = sentimentData.sentiment_analysis.map(s => s.negative_comments_pct);
    
    charts.sentiment = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: influencers,
            datasets: [
                {
                    label: 'Positive Comments (%)',
                    data: positiveComments,
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderWidth: 2
                },
                {
                    label: 'Negative Comments (%)',
                    data: negativeComments,
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function createReachChart(metricsData) {
    const canvas = document.getElementById('reachChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.reach) {
        charts.reach.destroy();
    }
    
    const influencers = metricsData.influencer_metrics.map(m => m.influencer_name);
    const totalLikes = metricsData.influencer_metrics.map(m => m.total_likes);
    const totalComments = metricsData.influencer_metrics.map(m => m.total_comments);
    
    charts.reach = new Chart(ctx, {
        type: 'line',
        data: {
            labels: influencers,
            datasets: [
                {
                    label: 'Total Likes',
                    data: totalLikes,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Total Comments',
                    data: totalComments,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            // CONTINUATION - Place this after the previous code

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createInfluencerTable(data) {
    const tableContainer = document.getElementById('influencerTable');
    if (!tableContainer) return;
    
    const combinedData = data.metrics.influencer_metrics.map(metric => {
        const credibility = data.credibility.credibility_analysis.find(
            c => c.influencer_name === metric.influencer_name
        );
        const sentiment = data.sentiment.sentiment_analysis.find(
            s => s.influencer_name === metric.influencer_name
        );
        
        return {
            ...metric,
            ...credibility,
            ...sentiment
        };
    });
    
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Influencer</th>
                    <th>Total Followers</th>
                    <th>Real Followers</th>
                    <th>Fake (%)</th>
                    <th>Engagement Rate</th>
                    <th>Credibility</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    combinedData.forEach(influencer => {
        const statusClass = influencer.credibility_status === 'High' ? 'status-high' : 
                          (influencer.credibility_status === 'Medium' ? 'status-medium' : 'status-low');
        
        const fakePercentage = influencer.fake_percentage || 0;
        const fakeClass = fakePercentage < 10 ? 'status-high' : 
                         (fakePercentage < 25 ? 'status-medium' : 'status-low');
        
        tableHTML += `
            <tr>
                <td><strong>${influencer.influencer_name}</strong></td>
                <td>${formatNumber(influencer.total_followers || 50000)}</td>
                <td>${formatNumber(influencer.estimated_real_followers || 45000)}</td>
                <td class="${fakeClass}">${fakePercentage.toFixed(1)}%</td>
                <td>${influencer.engagement_rate}%</td>
                <td>${(influencer.credibility_score * 100).toFixed(1)}%</td>
                <td class="${statusClass}">${influencer.credibility_status}</td>
                <td>
                    <button onclick="viewBrandRecommendationsForInfluencer('${influencer.influencer_name}')" 
                            style="padding: 8px 15px; background: #667eea; color: white; border: none; 
                            border-radius: 5px; cursor: pointer; font-weight: 600;">
                        View Brands
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    tableContainer.innerHTML = tableHTML;
}

async function viewBrandRecommendationsForInfluencer(influencerName) {
    document.getElementById('searchInput').value = influencerName;
    await searchInfluencer();
    
    setTimeout(() => {
        const recommendationsEl = document.getElementById('brandRecommendations');
        if (recommendationsEl) {
            recommendationsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 500);
}

function createEngagementChart(metricsData) {
    const canvas = document.getElementById('engagementChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.engagement) {
        charts.engagement.destroy();
    }
    
    const influencers = metricsData.influencer_metrics.map(m => m.influencer_name);
    const engagementRates = metricsData.influencer_metrics.map(m => m.engagement_rate);
    
    charts.engagement = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: influencers,
            datasets: [{
                label: 'Engagement Rate (%)',
                data: engagementRates,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Engagement Rate (%)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createCredibilityChart(credibilityData) {
    const canvas = document.getElementById('credibilityChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (charts.credibility) {
        charts.credibility.destroy();
    }
    
    const influencers = credibilityData.credibility_analysis.map(c => c.influencer_name);
    const scores = credibilityData.credibility_analysis.map(c => c.credibility_score * 100);
    
    charts.credibility = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: influencers,
            datasets: [{
                label: 'Credibility Score',
                data: scores,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgba(102, 126, 234, 1)',
                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}