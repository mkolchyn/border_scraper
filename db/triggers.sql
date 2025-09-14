CREATE TRIGGER trg_car_live_queue_insert
AFTER INSERT ON car_live_queue
FOR EACH ROW
EXECUTE FUNCTION calculate_queue_speed();