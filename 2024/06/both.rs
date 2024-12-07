use std::{collections::HashSet, env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<(HashSet<(usize, usize)>, (usize, usize), (usize, usize))> {
    let file = File::open(path)?;

    let mut start = (usize::max_value(), usize::max_value());
    let mut obstacles = HashSet::new();
    let mut height = 0;
    let mut width = 0;
    for (y, line) in io::BufReader::new(file).lines().enumerate() {
        let row = line?;
        height += 1;
        width = row.len();
        for (x, cell) in row.chars().enumerate() {
            match cell {
                '.' => (),
                '#' => { obstacles.insert((x, y)); },
                '^' => start = (x, y),
                _ => panic!("unexpected char in grid"),
            }
        }
    }

    Ok((obstacles, start, (width, height)))
}

fn simulate(obstacles: &HashSet<(usize, usize)>, start: (usize, usize), size: (usize, usize)) -> Option<HashSet<(usize, usize, i64, i64)>> {
    let mut visited = HashSet::with_capacity(size.0 * size.1);
    let mut guard = (start.0, start.1, 0, -1);
    while visited.insert(guard) {
        let (x, y, dx, dy) = guard;
        let nx = x.wrapping_add(dx as usize);
        let ny = y.wrapping_add(dy as usize);
        if obstacles.contains(&(nx, ny)) {
            guard = (x, y, -dy, dx);
        } else if nx < size.0 && ny < size.1 {
            guard = (nx, ny, dx, dy);
        } else {
            return Some(visited);
        }
    }
    None
}

fn solve(obstacles: HashSet<(usize, usize)>, start: (usize, usize), size: (usize, usize)) {
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
