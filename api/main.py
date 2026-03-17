from fastapi import FastAPI
import uvicorn
import dal 
from maps_data.DigitalHunter_map import plot_map_with_geometry
app = FastAPI()

@app.get("/quality-goal-shift-alert")
def quality_goal():
    query = dal.quality_goal_shift_alert
    return dal.run_query(query)

@app.get("/analysis_collection_sources")
def collection_sources():
    query = dal.analysis_collection_sources
    return dal.run_query(query)

@app.get("/finding_new_targets")
def new_targets():
    query = dal.finding_new_targets
    return dal.run_query(query)

@app.get("/extreme_behavioral_pattern")
def extreme_behavioral():
    query = dal.extreme_behavioral_pattern
    return dal.run_query(query)

# Auxiliary function for visual target display
@app.get("/all-entities")
def all_entities():
    query = dal.all_entities
    return dal.run_query(query)

@app.get("/visual_target_path/{entity_id}")
def visual_target(entity_id: str):
    res = dal.load_target_path(entity_id)
    plot_map_with_geometry(res)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)