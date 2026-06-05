// Search influencer functionality
async function searchInfluencer() {
    const username = document.getElementById('searchInput').value.trim();
    
    if (!username) {
        alert('Please enter an Instagram username');
        return;
    }
    
    showLoading();
    
    try {
        const response = await authenticatedFetch(`/api/search/${username}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displaySearchResults(data);
            await loadBrandRecommendations(username);
        } else {
            alert(data.message || 'Influencer not found');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to search influencer. Please try again.');
    } finally {
        hideLoading();
    }
}

function displaySearchResults(data) {
    const resultsDiv = document.getElementById('searchResults');
    const profile = data.profile_info;
    const metrics = data.metrics.influencer_metrics[0] || {};
    const credibility = data.credibility.credibility_analysis[0] || {};
    const sentiment = data.sentiment.sentiment_analysis[0] || {};
    
    const initial = profile.username.charAt(0).toUpperCase();
    
    resultsDiv.innerHTML = `
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">${initial}</div>
                <div>
                    <h2>@${profile.username}</h2>
                    <p style="color: #666;">Influencer Profile</p>
                </div>
            </div>
            
            <div class="profile-stats">
                <div class="stat-box">
                    <h4>${formatNumber(profile.followers_count)}</h4>
                    <p>Followers</p>
                </div>
                <div class="stat-box">
                    <h4>${formatNumber(profile.following_count)}</h4>
                    <p>Following</p>
                </div>
                <div class="stat-box">
                    <h4>${profile.total_posts}</h4>
                    <p>Posts</p>
                </div>
            </div>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <h3>Engagement Rate</h3>
                <p class="metric">${metrics.engagement_rate || 0}%</p>
            </div>
            <div class="card">
                <h3>Avg Likes</h3>
                <p class="metric">${formatNumber(metrics.total_likes || 0)}</p>
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
        
        <div class="chart-container">
            <h2>Recent Posts Preview</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                ${data.recent_posts.map(post => `
                    <div class="card">
                        <p><strong>❤️ ${formatNumber(post.likes)}</strong> likes</p>
                        <p><strong>💬 ${post.comments}</strong> comments</p>
                        <p style="font-size: 0.85em; color: #666; margin-top: 10px;">${post.caption}</p>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div id="brandRecommendations"></div>
    `;
    
    resultsDiv.style.display = 'block';
}

async function loadBrandRecommendations(username) {
    try {
        const response = await authenticatedFetch(`/api/brand-recommendations/${username}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayBrandRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Error loading brand recommendations:', error);
    }
}

function displayBrandRecommendations(rec) {
    const recDiv = document.getElementById('brandRecommendations');
    
    if (!rec || rec.error) {
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
                        <strong>Followers:</strong> ${formatNumber(rec.metrics_summary.followers)}
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