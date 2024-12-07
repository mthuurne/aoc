use std::{collections::HashSet, env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<(HashSet<(i64, i64)>, (i64, i64), (i64, i64))> {
    let file = File::open(path)?;

    let mut start = (-1, -1);
    let mut obstacles = HashSet::new();
    let mut height = 0;
    let mut width = -1;
    for (y, line) in io::BufReader::new(file).lines().enumerate() {
        let row = line?;
        height += 1;
        width = row.len() as i64;
        for (x, cell) in row.chars().enumerate() {
            match cell {
                '.' => {},
                '#' => { obstacles.insert((x as i64, y as i64)); },
                '^' => start = (x as i64, y as i64),
                _ => panic!("unexpected char in grid"),
            }
        }
    }

    Ok((obstacles, start, (width, height)))
}

fn simulate(obstacles: &HashSet<(i64, i64)>, start: (i64, i64), size: (i64, i64)) -> Option<HashSet<(i64, i64, i64, i64)>> {
    let mut visited = HashSet::new();
    let mut guard = (start.0, start.1, 0, -1);
    while visited.insert(guard) {
        let (x, y, dx, dy) = guard;
        let nx = x + dx;
        let ny = y + dy;
        if obstacles.contains(&(nx, ny)) {
            guard = (x, y, -dy, dx);
        } else if 0 <= nx && nx < size.0 && 0 <= ny && ny < size.1 {
            guard = (nx, ny, dx, dy);
        } else {
            return Some(visited);
        }
    }
    None
}

fn solve(obstacles: HashSet<(i64, i64)>, start: (i64, i64), size: (i64, i64)) {
    let mut visited = simulate(&obstacles, start, size).unwrap().iter().map(
        |(x, y, _dx, _dy)| (*x, *y)
    ).collect::<HashSet<_>>();
    println!("part 1: {}", visited.len());

    visited.remove(&start);
    let num_options = visited.into_iter().filter(|new_obstacle| {
        let mut new_obstacles = obstacles.clone();
        new_obstacles.insert(*new_obstacle);
        simulate(&new_obstacles, start, size).is_none()
    }).count();
    println!("part 2: {num_options}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let (obstacles, start, size ) =
            read_input(Path::new(&arg)).expect("reading input");
        solve(obstacles, start, size);
    }
}
