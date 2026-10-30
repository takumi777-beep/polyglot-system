use pyo3::prelude::*;
use rand::Rng;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

#[pyfunction]
fn update_agents(pos_x: Vec<f64>, pos_y: Vec<f64>, count: usize) -> PyResult<(Vec<f64>, Vec<f64>)> {
    let mut new_x = Vec::with_capacity(count);
    let mut new_y = Vec::with_capacity(count);
    let mut rng = rand::thread_rng();

    for i in 0..count {
        let dx = rng.gen_range(-2.0..2.0);
        let dy = rng.gen_range(-2.0..2.0);
        new_x.push(pos_x[i] + dx);
        new_y.push(pos_y[i] + dy);
    }
    Ok((new_x, new_y))
}

// 簡易的なゼロ知識証明
#[pyfunction]
fn prove_knowledge(secret_x: u64) -> PyResult<(u64, u64)> {
    let mut rng = rand::thread_rng();
    let r: u64 = rng.gen_range(1..1_000_000);
    let mut hasher = DefaultHasher::new();
    (secret_x + r).hash(&mut hasher);
    let commitment = hasher.finish();
    Ok((commitment, r))
}

#[pyfunction]
fn verify_knowledge(commitment: u64, r: u64, public_x: u64) -> PyResult<bool> {
    let mut hasher = DefaultHasher::new();
    (public_x + r).hash(&mut hasher);
    let calculated_commitment = hasher.finish();
    Ok(calculated_commitment == commitment)
}

#[pymodule]
fn ouroborosx_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(update_agents, m)?)?;
    m.add_function(wrap_pyfunction!(prove_knowledge, m)?)?;
    m.add_function(wrap_pyfunction!(verify_knowledge, m)?)?;
    Ok(())
}