/**
 * Interactive Tour Planner
 * Filter tours by dates, cost, terrain, support level
 */

export function initTourPlanner() {
  const plannerContainer = document.querySelector('.tour-planner');
  if (!plannerContainer) return;
  
  setupPlannerFilters(plannerContainer);
}

function setupPlannerFilters(container) {
  container.innerHTML = `
    <div class="planner-filters">
      <h3>Find Your Perfect Tour</h3>
      <form class="planner-form">
        <div class="form__group">
          <label for="planner-dates" class="form__label">Travel Dates</label>
          <input type="date" id="planner-dates" class="form__input" name="dates">
        </div>
        
        <div class="form__group">
          <label for="planner-cost-min" class="form__label">Budget Range</label>
          <div style="display: flex; gap: var(--space-2);">
            <input type="number" id="planner-cost-min" class="form__input" placeholder="Min" name="costMin">
            <input type="number" id="planner-cost-max" class="form__input" placeholder="Max" name="costMax">
          </div>
        </div>
        
        <div class="form__group">
          <label for="planner-terrain" class="form__label">Terrain Type</label>
          <select id="planner-terrain" class="form__select" name="terrain">
            <option value="">All Terrains</option>
            <option value="paved">Paved Roads</option>
            <option value="mixed">Mixed (Paved & Off-road)</option>
            <option value="offroad">Off-road</option>
          </select>
        </div>
        
        <div class="form__group">
          <label for="planner-support" class="form__label">Support Level</label>
          <select id="planner-support" class="form__select" name="support">
            <option value="">All Levels</option>
            <option value="basic">Basic Support</option>
            <option value="standard">Standard Support</option>
            <option value="premium">Premium Support</option>
          </select>
        </div>
        
        <div class="form__group">
          <label for="planner-offroad" class="form__label">Off-roading Level</label>
          <select id="planner-offroad" class="form__select" name="offroadLevel">
            <option value="">Any Level</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        
        <button type="submit" class="btn btn--primary">Find Tours</button>
        <button type="reset" class="btn btn--secondary">Reset</button>
      </form>
    </div>
    
    <div class="planner-results" id="planner-results"></div>
  `;
  
  const form = container.querySelector('.planner-form');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const filters = getFilters(form);
    filterTours(filters);
  });
}

function getFilters(form) {
  const formData = new FormData(form);
  return {
    dates: formData.get('dates'),
    costMin: formData.get('costMin'),
    costMax: formData.get('costMax'),
    terrain: formData.get('terrain'),
    support: formData.get('support'),
    offroadLevel: formData.get('offroadLevel'),
  };
}

function filterTours(filters) {
  // This would filter tours based on criteria
  const resultsContainer = document.getElementById('planner-results');
  if (resultsContainer) {
    resultsContainer.innerHTML = '<p>Filtering tours...</p>';
    // In production, this would call an API or filter local data
  }
}

export default { initTourPlanner };
