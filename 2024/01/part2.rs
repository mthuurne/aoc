use std::{collections::HashMap, env, fs::File, io, io::BufRead, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<(i64, i64)>> {
    let file = File::open(path)?;
    let mut data: Vec<(i64, i64)> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        let values = Vec::from_iter(line?.split_whitespace().map(
            |s| s.parse().expect("values must be integers")
        ));
        match &values[..] {
            &[first, second, ..] => data.push((first, second)),
            _ => panic!("input must have two values per line"),
        };
    }
    Ok(data)
}

fn solve(data: &Vec<(i64, i64)>) {
    let mut freqs: HashMap<i64, usize> = HashMap::new();
    for (_, x) in data {
        *freqs.entry(*x).or_insert(0) += 1
    }
    let total_delta: usize = data.iter().map(|(x, _)| *freqs.get(x).unwrap()).sum();
    println!("{total_delta}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    for arg in &args[1..] {
        println!("=== {arg}");
        let data = read_input(Path::new(arg)).expect("reading input");
        solve(&data);
    }
}
